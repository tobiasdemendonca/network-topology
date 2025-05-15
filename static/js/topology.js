// Network Topology Visualization using D3.js
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const svg = d3.select('#topology-svg');
    const uploadForm = document.getElementById('upload-form');
    const fileUpload = document.getElementById('file-upload');
    const loadDemoBtn = document.getElementById('load-demo-btn');
    const nodeDetails = document.getElementById('node-details');
    const zoomSlider = document.getElementById('zoom-slider');
    const nodeDistanceSlider = document.getElementById('node-distance');
    const chargeStrengthSlider = document.getElementById('charge-strength');
    
    // Initialize variables
    let width = document.getElementById('topology-container').clientWidth;
    let height = document.getElementById('topology-container').clientHeight;
    let simulation;
    let nodes = [];
    let links = [];
    let zoom;
    
    // Set up the SVG container and groups
    const g = svg.append('g');
    
    // Create groups for links and nodes (to ensure proper layering)
    const linksGroup = g.append('g').attr('class', 'links');
    const nodesGroup = g.append('g').attr('class', 'nodes');
    const labelsGroup = g.append('g').attr('class', 'labels');
    
    // SVG defs for markers (arrowheads)
    const defs = svg.append('defs');
    defs.append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '-0 -5 10 10')
        .attr('refX', 20)
        .attr('refY', 0)
        .attr('orient', 'auto')
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('xoverflow', 'visible')
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke', 'none');
    
    // Create a pattern for subnet nodes with white background
    const subnetPattern = defs.append('pattern')
        .attr('id', 'subnet-pattern')
        .attr('patternUnits', 'objectBoundingBox')
        .attr('width', 1)
        .attr('height', 1);

    // Add white background rectangle (covers the entire circle)
    subnetPattern.append('rect')
        .attr('width', 100)
        .attr('height', 100)
        .attr('fill', 'white');

    // Add the image on top with centering offsets
    subnetPattern.append('image')
        .attr('xlink:href', '/static/images/cloud.svg')
        .attr('width', 45)  // Slightly smaller than the background
        .attr('height', 45)
        .attr('x', 12,5)  // Center horizontally: (30-25)/2 = 2.5
        .attr('y', 12.5);  // Center vertically: (30-25)/2 = 2.5

    // Set up zoom behavior
    function setupZoom() {
        zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on('zoom', (event) => {
                g.attr('transform', event.transform);
            });
        
        svg.call(zoom);
    }
    
    // Update visualization on window resize
    window.addEventListener('resize', function() {
        width = document.getElementById('topology-container').clientWidth;
        height = document.getElementById('topology-container').clientHeight;
        
        if (simulation) {
            simulation.alpha(0.3).restart();
        }
    });
    
    // Initialize the force simulation
    function initializeSimulation() {
        simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links).id(d => d.id).distance(200))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(50))
            .on('tick', ticked);
    }
    
    // Update node and link positions on each tick
    function ticked() {
        d3.selectAll('.link')
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        
        d3.selectAll('.node')
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
        
        d3.selectAll('.node-label')
            .attr('x', d => d.x)
            .attr('y', d => {
            // Use a larger Y-offset for subnet nodes
            return d.type === 'subnet' ? d.y + 50 : d.y + 30;
        });
    }
    
    // Create tooltip for hover information
    const tooltip = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0);
    
    // Render the network topology visualization
    function renderTopology(data) {
        // Clear existing content
        linksGroup.selectAll('*').remove();
        nodesGroup.selectAll('*').remove();
        labelsGroup.selectAll('*').remove();
        
        // Update nodes and links with the new data
        nodes = data.nodes;
        links = data.links;
        
        // Re-initialize the simulation with new data
        initializeSimulation();
        
        // Draw links
        const link = linksGroup.selectAll('.link')
            .data(links)
            .enter().append('line')
            .attr('class', 'link')
            .attr('marker-end', 'url(#arrowhead)')
            .on('mouseover', function(event, d) {
                tooltip.transition()
                    .duration(200)
                    .style('opacity', .9);
                tooltip.html(`Interface: ${d.interface}<br>IP: ${d.ip}`)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY - 28) + 'px');
            })
            .on('mouseout', function() {
                tooltip.transition()
                    .duration(500)
                    .style('opacity', 0);
            });
        
        // Draw nodes
        const node = nodesGroup.selectAll('.node')
            .data(nodes)
            .enter().append('circle')
            .attr('class', d => {
                const nodeType = d.type === 'node' ? 'machine' : d.type;
                return `node ${nodeType}`;
            })
            .attr('r', function(d) {
                if (d.type === 'subnet') {
                    return 35;
                } else {
                    return 15;
                }
            })
            .style("fill", function (d) {
                if (d.type === 'subnet') {
                    return 'url(#subnet-pattern)';
                } else {
                    return d.fill_color;
                }
            })
            .on('click', function(event, d) {
                // Display node details in the sidebar
                showNodeDetails(d);
                
                // Highlight the node
                d3.selectAll('.node').classed('selected', false);
                d3.select(this).classed('selected', true);
            })
            .on('mouseover', function(event, d) {
                tooltip.transition()
                    .duration(200)
                    .style('opacity', .9);
                    
                let tooltipText = `<strong>Name</strong><br>${d.name}`;
                if (d.type === 'subnet') {
                    tooltipText += `<br><br><strong>CIDR</strong><br>${d.cidr}`;
                } else if (d.type === 'node') {
                    tooltipText += `<br><br><strong>Interfaces</strong>`;
                    d.interfaces.forEach(intf => {
                        tooltipText += `<br>${intf.name}: ${intf.ip}`;
                    });
                }
                
                tooltip.html(tooltipText)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY - 28) + 'px');
            })
            .on('mouseout', function() {
                tooltip.transition()
                    .duration(500)
                    .style('opacity', 0);
            })
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        // Add labels to nodes
        const label = labelsGroup.selectAll('.node-label')
            .data(nodes)
            .enter().append('text')
            .attr('class', 'node-label')
            .text(d => d.name);
        
        // Add node dragging behavior
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
        
    }
    
    // Display node details in the sidebar
    function showNodeDetails(node) {
        let details = `<h3>${node.name}</h3>`;
        
        if (node.type === 'subnet') {
            details += `<p><strong>Type:</strong> Subnet</p>`;
            details += `<p><strong>CIDR:</strong> ${node.cidr}</p>`;
            
            // Find all nodes connected to this subnet
            const connectedNodes = links.filter(link => link.target.id === node.id)
                .map(link => link.source.name);
            
            if (connectedNodes.length > 0) {
                details += `<p><strong>Connected Nodes:</strong></p>`;
                details += `<ul>`;
                connectedNodes.forEach(nodeName => {
                    details += `<li>${nodeName}</li>`;
                });
                details += `</ul>`;
            }
        } else {
            details += `<p><strong>Type:</strong> Node</p>`;
            
            // Find all interfaces for this node
            const nodeInterfaces = links.filter(link => link.source.id === node.id);
            
            if (nodeInterfaces.length > 0) {
                details += `<p><strong>Interfaces:</strong></p>`;
                details += `<ul>`;
                nodeInterfaces.forEach(link => {
                    details += `<li>${link.interface}: ${link.ip} (connected to ${link.target.name})</li>`;
                });
                details += `</ul>`;
            }
        }
        
        nodeDetails.innerHTML = details;
    }
    
    // Load demo data
    function loadDemoData() {
        fetch('/api/topology')
            .then(response => response.json())
            .then(data => {
                renderTopology(data);
            })
            .catch(error => {
                console.error('Error loading demo data:', error);
                alert('Failed to load demo data. Please try again.');
            });
    }
    
    // Initialize the visualization
    function init() {
        setupZoom();
        
        // Load demo data when clicking the demo button
        loadDemoBtn.addEventListener('click', loadDemoData);
        
        // Handle file upload
        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const file = fileUpload.files[0];
            if (!file) {
                alert('Please select a file to upload');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            let endpoint;
            if (file.name.endsWith('.json')) {
                endpoint = '/api/load-json';
            } else if (file.name.endsWith('.yaml') || file.name.endsWith('.yml')) {
                endpoint = '/api/load-yaml';
            } else {
                alert('Unsupported file format. Please upload a JSON or YAML file.');
                return;
            }
            
            fetch(endpoint, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                renderTopology(data);
            })
            .catch(error => {
                console.error('Error uploading file:', error);
                alert('Failed to upload and process the file. Please check the file format.');
            });
        });
        
        // Handle zoom slider
        zoomSlider.addEventListener('input', function() {
            const scale = parseFloat(this.value);
            svg.call(zoom.transform, d3.zoomIdentity.scale(scale));
        });
        
        // Handle node distance slider
        nodeDistanceSlider.addEventListener('input', function() {
            const distance = parseInt(this.value);
            simulation.force('link').distance(distance);
            simulation.alpha(0.3).restart();
        });
        
        // Handle charge strength slider
        chargeStrengthSlider.addEventListener('input', function() {
            const strength = parseInt(this.value);
            simulation.force('charge').strength(strength);
            simulation.alpha(0.3).restart();
        });
        
        // Load demo data initially
        loadDemoData();
    }
    
    // Call the init function to start the visualization
    init();
}); 