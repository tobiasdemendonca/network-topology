# Network Topology Visualization

A web-based network topology visualization tool inspired by OpenStack Horizon's network topology visualization. This tool allows you to upload network topology data in YAML or JSON format and visualize it in an interactive graph.

## Features

- Interactive network visualization with D3.js force-directed graph
- Upload network data in YAML or JSON format
- Interactive controls for zooming, node distance, and charge strength
- Node and link details on hover and click
- Responsive design that works on desktop and mobile devices
- Demo data included for quick start

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/network-topology.git
   cd network-topology
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

### Loading Demo Data

Click the "Load Demo Data" button to load a sample network topology for demonstration.

### Uploading Your Own Data

1. Prepare your network data in either YAML or JSON format (see format examples below).
2. Click the "Browse" button and select your file.
3. Click "Upload & Visualize" to display your network topology.

### Controlling the Visualization

- **Zoom**: Use the zoom slider or mouse wheel to zoom in and out.
- **Node Distance**: Adjust the distance between nodes using the "Node Distance" slider.
- **Charge Strength**: Control the repulsion force between nodes with the "Charge Strength" slider.
- **Dragging**: Click and drag nodes to reposition them.
- **Node Details**: Click on a node to view its details in the sidebar.

## Data Format

### YAML Format Example

```yaml
node1:
  hostname: server1
  ip: 192.168.1.10
  subnet: 192.168.1.0/24
node2:
  hostname: server2
  ip: 192.168.1.11
  subnet: 192.168.1.0/24
node3:
  hostname: router1
  ip: 192.168.2.1
  subnet: 192.168.2.0/24
```

### JSON Format Example

The JSON format should match the internal D3.js format:

```json
{
  "nodes": [
    {
      "id": "Subnet_1",
      "name": "Subnet 1",
      "cidr": "192.168.1.0/24",
      "type": "subnet",
      "group": 1
    },
    {
      "id": "Node_1",
      "name": "Node 1",
      "type": "node",
      "group": 2
    }
  ],
  "links": [
    {
      "source": "Node_1",
      "target": "Subnet_1",
      "interface": "eth0",
      "ip": "192.168.1.10"
    }
  ]
}
```

## Extending the Application

You can extend the application by:

1. Adding more node types (e.g., firewalls, load balancers)
2. Supporting additional data formats
3. Implementing additional visualization features
4. Adding backend integration to fetch network data from external sources

## Technology Stack

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Visualization: D3.js
- Data Formats: JSON, YAML

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by [OpenStack Horizon's Network Topology](https://opendev.org/openstack/horizon/src/branch/master/openstack_dashboard/dashboards/project/network_topology) visualization
- Uses [D3.js](https://d3js.org/) for interactive data visualization 