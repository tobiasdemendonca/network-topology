#!/usr/bin/env python3
from __future__ import annotations
import yaml
from pathlib import Path
import mmap
from ipaddress import IPv4Network, IPv4Address
import argparse

class Node:
    def __init__(
        self,
        system_id: str,
        hostname: str,
        interfaces: set[NetworkInterface],
    ) -> None:
        self.system_id = system_id
        self.hostname = hostname
        self.interfaces = interfaces
    
    def to_mermaid(self) -> str:
        return f"{self.system_id}[Node_{self.system_id}<br>hostname={self.hostname}]"
    
    def __str__(self):
        output = f"Node(system_id={self.system_id}, hostname={self.hostname})\n"
        for interface in self.interfaces:
            output += f"\t{interface}\n"
        return output

class Subnet:
    def __init__(
        self,
        id: int,
        cidr: IPv4Network
    ) -> None:
        self.id = id
        self.cidr = cidr
    
    def to_mermaid(self) -> str:
        # id() is used to get a unique identifier for the subnet
        # as i don't know how to reformat the cidr nicely
        return f"Subnet_{self.id}[Subnet_{self.id}<br>{self.cidr}]"
    
    def __str__(self):
        return f"Subnet_{self.id}(cidr={self.cidr})"
    
    def __eq__(self, other: Subnet) -> bool:
        if not isinstance(other, Subnet):
            return False
        return self.id == other.id and self.cidr == other.cidr

    def __hash__(self) -> int:
        return hash(self.id)

    def __ne__(self, other: Subnet) -> bool:
        if not isinstance(other, Subnet):
            return True
        return self.id != other.id or self.cidr != other.cidr

class NetworkInterface: 
    def __init__(
        self,
        name: str,
        ipaddress: IPv4Address | None,
        subnet: Subnet,
    ) -> None: 
        self.name = name
        self.ipaddress = ipaddress
        self.subnet = subnet

    def to_mermaid(self) -> str:
        if self.ipaddress is None:
            return "DHCP lease expired"
        return f"{self.name}: {self.ipaddress}"
        
    def __repr__(self) -> str:
        return f"NetworkInterface(name={self.name}, ipaddress={self.ipaddress}, subnet={self.subnet})"

class Network:
    def __init__(self, nodes: set[Node], subnets: set[Subnet]) -> None: 
        self.nodes = nodes
        self.subnets = subnets
    
    def __str__(self) -> str:
        output = "Network:\n"
        for node in self.nodes:
            output += f"\t{node}\n"
        for subnet in self.subnets:
            output += f"\t{subnet}\n"
        return output
        
    @classmethod
    def from_yaml(cls, yaml_file: Path) -> Network:
        known_subnets = set()
        nodes = set()

        new_subnet_id = 0

        with open(yaml_file, "r") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                data = yaml.safe_load(mm.read())
                for k in data:
                    for data_subnet in data[k]["subnets"]:
                        subnet_exists = False
                        for known_subnet in known_subnets:
                            if IPv4Network(data_subnet) == known_subnet.cidr:
                                subnet_exists = True
                                break
                        if not subnet_exists:
                            sn = Subnet(new_subnet_id, IPv4Network(data_subnet))
                            new_subnet_id += 1
                            known_subnets.add(sn)

                    node_interfaces = set()
                    for idx, data_ip in enumerate(data[k]["ips"]):
                        ip = None if data_ip == "None" else IPv4Address(data_ip)
                        ni = NetworkInterface("", ip, None)
                        sn_data = data[k]["subnets"][idx]

                        for sn in known_subnets:
                            if IPv4Network(sn_data) == sn.cidr:
                                ni.subnet = sn
                                break

                        node_interfaces.add(ni)

                    n = Node(k, data[k]["hostname"], node_interfaces)
                    nodes.add(n)

        # print("Subnets:")
        # for sn in known_subnets:
        #     print("\t", sn)
        
        # print("Nodes:")
        # for n in nodes:
        #     print("\t", n)
        
        return Network(nodes, known_subnets)

class MermaidOutputter:
    @staticmethod
    def construct_mermaid(network: Network) -> str:
        output = "graph LR\n\n"

        # Write out the subnets first as they're independent
        for subnet in network.subnets:
            output += f"  {subnet.to_mermaid()}\n"

        output += "\n"

        # Nodes are in subnets to write them next
        for node in network.nodes:
            output += f"  {node.to_mermaid()}\n"
        output += "\n"

        # Then finish by writing out the connections between nodes and their subnets
        for node in network.nodes:
            # TODO: Get network interface name

            for interface in node.interfaces:
                output += f"  {node.system_id} -->"
                output += f"|{interface.to_mermaid()}|"
                output += f" {interface.subnet.to_mermaid()}\n"

        return output

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a mermaid diagram from a network yaml file"
    )
    parser.add_argument(
        "yaml_file",
        type=Path,
        help="The yaml file to read the network from"
    )
    return parser

def main(yaml_file: Path) -> None:

    print(
        MermaidOutputter.construct_mermaid(
            Network.from_yaml(yaml_file)
        )
    )
    
    
if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    if args.yaml_file:
        main(args.yaml_file)
    else:
        raise Exception("No yaml file provided")
    