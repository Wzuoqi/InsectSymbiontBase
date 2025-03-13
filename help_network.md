# Network Visualization Guide

## Overview

The Network Visualization tool provides an interactive interface for exploring the relationships between insect hosts and their symbionts. This tool visualizes symbiotic relationships extracted from scientific literature, allowing researchers to discover and analyze host-symbiont interaction patterns.

## Features

### Network Components

#### Nodes
- **Host Nodes (Orange)**
  - Represents insect host species
  - Size indicates number of symbiont connections
  - Clickable for detailed host information

- **Symbiont Nodes (Blue)**
  - Represents symbiont genera
  - Size reflects frequency in database
  - Special colors for vital symbiotic genera
  - Links to symbiont records

#### Edges
- Represents documented symbiotic relationships
- Line thickness indicates relationship strength
- Clickable for detailed symbiosis information
- Curved design for better visualization

### Interactive Features

#### Node Interactions
1. **Hover Effects**
   - Highlights connected nodes and edges
   - Shows node details in tooltip:
     - Node name
     - Number of connections
     - Type (Host/Symbiont)

2. **Click Actions**
   - Host nodes: Opens species detail page
   - Symbiont nodes: Shows all related records
   - Maintains highlight state for exploration

3. **Drag Functionality**
   - Nodes can be dragged for custom layout
   - Network automatically adjusts
   - Position changes persist during session

#### Edge Interactions
1. **Hover Effects**
   - Emphasizes the connection
   - Shows relationship details
   - Highlights connected nodes

2. **Click Actions**
   - Opens detailed symbiosis record
   - Shows all documented interactions
   - Provides literature references

### Search and Navigation

#### Search Function
- Real-time node search
- Supports partial name matching
- Case-insensitive search
- Results highlighted with golden glow
- Shows number of matching nodes

#### View Controls
- Zoom in/out capability
- Pan across network
- Reset view option
- Fit to screen function

### Visual Customization

#### Layout Options
- Force-directed layout
- Adjustable node spacing
- Automatic edge routing
- Collision detection

#### Display Settings
- Node size scaling
- Edge thickness adjustment
- Label visibility toggle
- Color scheme options

## Usage Guide

### Getting Started

1. **Initial View**
   - Network loads with optimized layout
   - Nodes are colored by type
   - Size indicates connection count
   - Wait for full loading before interaction

2. **Basic Navigation**
   - Use mouse wheel to zoom
   - Click and drag background to pan
   - Double-click to reset view
   - Use search for quick access

### Advanced Features

#### Network Analysis
1. **Finding Connections**
   - Search for specific nodes
   - Hover to highlight connections
   - Click to maintain highlight
   - Explore connected nodes

2. **Pattern Discovery**
   - Identify hub nodes
   - Find common associations
   - Explore taxonomic patterns
   - Analyze relationship clusters

#### Data Export
- Screenshot capability
- Node position saving
- Connection data export
- Custom view sharing

## Best Practices

### Performance Tips
1. **Optimal Viewing**
   - Use recommended browsers
   - Wait for complete loading
   - Limit active highlights
   - Clear search when done

2. **Navigation Efficiency**
   - Use search for specific nodes
   - Combine hover and click
   - Maintain reasonable zoom level
   - Reset view when lost

### Analysis Workflow
1. **Systematic Exploration**
   - Start with known nodes
   - Explore connections gradually
   - Document interesting patterns
   - Verify findings in detail pages

2. **Pattern Recognition**
   - Look for hub nodes
   - Note recurring connections
   - Identify unique patterns
   - Compare across taxa

## Troubleshooting

### Common Issues

1. **Loading Problems**
   ```
   Note: The network visualization contains a large dataset and may take a moment to load.
   We recommend waiting until the visualization is fully loaded before interacting.
   ```
   - Solutions:
     - Refresh page
     - Clear browser cache
     - Check internet connection
     - Use recommended browser

2. **Interaction Issues**
   - Reset view if lost
   - Clear search results
   - Refresh for new layout
   - Check browser compatibility

3. **Visual Glitches**
   - Zoom out and in
   - Reset network view
   - Refresh browser
   - Update graphics drivers

### Browser Support
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Requires WebGL support
- JavaScript enabled

## Technical Details

### Implementation
- ECharts visualization library
- Force-directed layout algorithm
- Real-time interaction handling
- Responsive design support

### Performance
- Progressive loading
- Efficient data structures
- Optimized rendering
- Memory management

### Data Updates
- Regular database updates
- New relationship additions
- Literature-based validation
- Quality control checks

## Future Enhancements

Planned features include:
- Advanced filtering options
- Custom layout saving
- Relationship type filtering
- Statistical analysis tools
- Batch data export
- Time-based visualization
- Taxonomic hierarchy view
- Integration with other tools
