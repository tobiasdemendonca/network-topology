import json

import yaml
from flask import Flask, jsonify, render_template, request

from network import Network, NetworkInterface, Node, Subnet

app = Flask(__name__)


@app.route("/")
def index():
    """Render the main page with the network topology visualization."""
    return render_template("index.html")


@app.route("/api/topology", methods=["GET"])
def get_topology():
    """API endpoint to get the topology data."""
    # For demonstration, we'll use the example network from network.py
    # In a real application, you might fetch this from a database or external service
    # subnet1 = Subnet(name="Subnet 1", cidr="192.168.1.0/24")
    # subnet2 = Subnet(name="Subnet 2", cidr="192.168.2.0/24")
    # subnet3 = Subnet(name="Subnet 3", cidr="192.168.3.0/24")

    # interface1 = NetworkInterface(name="eth0", ipaddress="192.168.1.10", subnet=subnet1)
    # interface2 = NetworkInterface(name="eth1", ipaddress="192.168.1.11", subnet=subnet1)
    # interface3 = NetworkInterface(name="eth2", ipaddress="192.168.2.10", subnet=subnet2)
    # interface4 = NetworkInterface(name="eth3", ipaddress=None, subnet=subnet3)

    # node1 = Node(name="Node 1", interfaces=[interface1, interface2, interface3])
    # node2 = Node(name="Node 2", interfaces=[interface4])

    network = Network(
        nodes=[], subnets=[]
    )  # Network(nodes=[node1, node2], subnets=[subnet1, subnet2, subnet3])

    # Convert to a format suitable for D3.js force-directed graph
    nodes = []
    links = []

    # Add subnets as nodes
    for subnet in network.subnets:
        nodes.append(
            {
                "id": subnet.name_without_spaces,
                "name": subnet.name,
                "cidr": subnet.cidr,
                "type": "subnet",
                "group": 1,
            }
        )

    # Add compute nodes
    for node in network.nodes:
        nodes.append(
            {
                "id": node.name_without_spaces,
                "name": node.name,
                "type": "node",
                "group": 2,
            }
        )

    # Add links between nodes and subnets
    for node in network.nodes:
        for interface in node.interfaces:
            links.append(
                {
                    "source": node.name_without_spaces,
                    "target": interface.subnet.name_without_spaces,
                    "interface": interface.name,
                    "ip": interface.ipaddress,
                }
            )

    return jsonify({"nodes": nodes, "links": links})


@app.route("/api/load-yaml", methods=["POST"])
def load_yaml():
    """Load a YAML file with network topology information."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith((".yaml", ".yml")):
        yaml_data = yaml.safe_load(file.stream)

        # Process YAML data into our network format
        subnets_dict = {}
        nodes = []

        for key, host_data in yaml_data.items():
            subnets = host_data.get("subnets", [])
            ips = host_data.get("ips", [])
            if len(subnets) != len(ips):
                return jsonify({"error": "Mismatch between subnets and IPs"}), 400

            for subnet_cidr in subnets:
                if subnet_cidr not in subnets_dict:
                    subnet_name = f"Subnet {len(subnets_dict) + 1}"
                    subnets_dict[subnet_cidr] = Subnet(
                        name=subnet_name, cidr=subnet_cidr
                    )

            interfaces = []
            for subnet_cidr, ip_addr in zip(subnets, ips):
                iface = NetworkInterface(
                    name="",
                    ipaddress=ip_addr if ip_addr != "None" else None,
                    subnet=subnets_dict[subnet_cidr],
                )
                interfaces.append(iface)

            node = Node(name=host_data.get("hostname") or key, interfaces=interfaces)
            nodes.append(node)

        network = Network(nodes=nodes, subnets=list(subnets_dict.values()))

        # Convert to D3.js format
        d3_nodes = []
        d3_links = []

        for subnet in network.subnets:
            d3_nodes.append(
                {
                    "id": subnet.name_without_spaces,
                    "name": subnet.name,
                    "cidr": subnet.cidr,
                    "type": "subnet",
                    "group": 1,
                }
            )

        for node in network.nodes:
            d3_nodes.append(
                {
                    "id": node.name_without_spaces,
                    "name": node.name,
                    "interfaces": [
                        {
                            "name": interface.name,
                            "ip": interface.ipaddress,
                        }
                        for interface in node.interfaces
                    ],
                    "type": "node",
                    "group": 2,
                }
            )

        for node in network.nodes:
            for interface in node.interfaces:
                d3_links.append(
                    {
                        "source": node.name_without_spaces,
                        "target": interface.subnet.name_without_spaces,
                        "interface": interface.name,
                        "ip": interface.ipaddress,
                    }
                )

        return jsonify({"nodes": d3_nodes, "links": d3_links})

    return jsonify({"error": "Invalid file format"}), 400


@app.route("/api/load-json", methods=["POST"])
def load_json():
    """Load a JSON file with network topology information."""
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith(".json"):
        try:
            json_data = json.load(file.stream)
            return jsonify(json_data)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format"}), 400

    return jsonify({"error": "Invalid file format"}), 400


if __name__ == "__main__":
    app.run(debug=True)
