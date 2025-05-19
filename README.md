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

The data format is currently not stable. Check [data/](./data/) for examples.

## Acknowledgments

- Inspired by [OpenStack Horizon's Network Topology](https://opendev.org/openstack/horizon/src/branch/master/openstack_dashboard/dashboards/project/network_topology) visualization
- Uses [D3.js](https://d3js.org/) for interactive data visualization 