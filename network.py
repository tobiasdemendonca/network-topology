from __future__ import annotations
import json

class NetworkInterface: 
    def __init__(self, name: str, ipaddress: str, subnet: Subnet) -> None: 
        self.name = name
        self.ipaddress = ipaddress
        self.subnet = subnet
        
    def __repr__(self) -> str:
        return f"NetworkInterface(name={self.name}, ipaddress={self.ipaddress}, subnet={self.subnet})"

class Node: 
    def __init__(self, name: str, interfaces: list[NetworkInterface]) -> None: 
        self.name = name
        self.interfaces = interfaces

    @property
    def name_without_spaces(self) -> str:
        return self.name.replace(' ', '_')
        
    def __repr__(self) -> str:
        return f"Node(name={self.name}, interfaces={self.interfaces})"

class Subnet: 
    def __init__(self, name: str, cidr: str) -> None:
        self.name = name
        self.cidr = cidr

    @property
    def name_without_spaces(self) -> str:
        return self.name.replace(" ", "_")
    
    def __repr__(self) -> str:
        return f"Subnet(name={self.name}, cidr={self.cidr})"
    
class Network:
    def __init__(self, nodes: list[Node], subnets: list[Subnet]) -> None: 
        self.nodes = nodes
        self.subnets = subnets
        
    @classmethod
    def from_json(cls, json_data: dict) -> Network: 
        return Network(**json_data)

class Outputer:
    
    def _start_string(self) -> str:
        return "graph TD\n\n"
    
    def output(self, network: Network) -> str:
        out  = self._start_string()
        
        for subnet in network.subnets:
            out += f"  {subnet.name_without_spaces}[\"{subnet.name}<br>{subnet.cidr}\"]\n"           
        
        out += "\n\n"
        
        for node in network.nodes:
            out += f"  {node.name_without_spaces}[\"{node.name}\"]\n"

        out += "\n\n"
        
        for node in network.nodes:
            for interface in node.interfaces:
                out += f"  {node.name_without_spaces} -->|"
                out += f"{interface.name}: {interface.ipaddress}"
                out += f"| {interface.subnet.name_without_spaces}"
                out += '\n'
            out += '\n'
            
        return out
        

def main():
    
    subnet1 = Subnet(name="Subnet 1", cidr="192.168.1.0/24")
    subnet2 = Subnet(name="Subnet 2", cidr="192.168.2.0/24")

    interface1 = NetworkInterface(name="eth0", ipaddress="192.168.1.10", subnet=subnet1)
    interface2 = NetworkInterface(name="eth1", ipaddress="192.168.1.11", subnet=subnet1)
    interface3 = NetworkInterface(name="eth2", ipaddress="192.168.2.10", subnet=subnet2)

    node1 = Node(name="Node 1", interfaces=[interface1, interface2, interface3])

    subnet3 = Subnet(name="Subnet 3", cidr="192.168.3.0/24")
    interface4 = NetworkInterface(name="eth3", ipaddress="192.168.3.10", subnet=subnet3)

    node2 = Node(name="Node 2", interfaces=[interface4])
    
    network = Network(nodes=[node1, node2], subnets=[subnet1, subnet2, subnet3])
    outputer = Outputer()
    print(outputer.output(network))
    
    # with open("network.json") as f:
    #     data = json.load(f)

    #     network = Network.from_json(data)
    #     outputer = Outputer()
    #     outputer.output(network)
    
if __name__ == "__main__":
    main()
    