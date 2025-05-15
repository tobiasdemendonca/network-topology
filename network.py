#!/usr/bin/env python3
from __future__ import annotations
import yaml
from pathlib import Path
import mmap

class Node:
    def __init__(self, system_id: str, hostname: str, ip: str, subnet: Subnet) -> None:
        self.system_id = system_id
        self.hostname = hostname
        self.ip = ip
        self.subnet = subnet
    
    def to_mermaid(self) -> str:
        return f"{self.system_id}[Node_{self.system_id}<br>hostname={self.hostname}]"
    
    def __str__(self):
        return f"Node(system_id={self.system_id}, hostname={self.hostname}, ip={self.ip}, subnet={self.subnet})"

class Subnet:
    def __init__(self, id: int, cidr: str) -> None:
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
        return self.cidr == other.cidr

    def __hash__(self) -> int:
        return hash(self.cidr)

    def __ne__(self, value):
        if not isinstance(value, Subnet):
            return True
        return self.cidr != value.cidr

class NetworkInterface: 
    def __init__(self, name: str, ipaddress: str, subnet: Subnet) -> None: 
        self.name = name
        self.ipaddress = ipaddress
        self.subnet = subnet
        
    def __repr__(self) -> str:
        return f"NetworkInterface(name={self.name}, ipaddress={self.ipaddress}, subnet={self.subnet})"

class Network:
    def __init__(self, nodes: set[Node], subnets: set[Subnet]) -> None: 
        self.nodes = nodes
        self.subnets = subnets
        
    @classmethod
    def from_yaml(cls, yaml_file: Path) -> Network:
        known_subnets = set()
        nodes = set()

        subnet_id = 0

        with open(yaml_file, "r") as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                data = yaml.safe_load(mm.read())
                for k in data:
                    sn = Subnet(0, data[k]["subnet"])
                    if sn not in known_subnets:
                        sn.id = subnet_id
                        subnet_id += 1
                        known_subnets.add(sn)
                    n = Node(k, data[k]["hostname"], data[k]["ip"], sn)
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

            # TODO: Clean up getting a subnet
            sn = None
            for subnet in network.subnets:
                if node.subnet == subnet:
                    sn = subnet
                    break
            output += f"  {node.system_id} -->|{node.ip}| {sn.to_mermaid()}\n"

        return output

def main():
    print(
        MermaidOutputter.construct_mermaid(
            Network.from_yaml("example-network.yaml")
        )
    )
    
    
if __name__ == "__main__":
    main()
    