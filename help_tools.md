# iSymBase Analysis Tools Guide

## Overview

iSymBase provides a comprehensive suite of analysis tools to help researchers explore and analyze insect symbiont data. Each tool is designed for specific analysis needs and workflows.

## Available Tools

### 1. BLAST Search

#### Description
BLAST (Basic Local Alignment Search Tool) allows users to compare query sequences against our database of insect symbiont sequences.

#### Features
- Multiple BLAST methods (blastn, tblastn)
- Specialized databases:
  - Symbiont Genome: Complete genome sequences from verified insect symbionts
  - Genes from Genome: Annotated genes from complete genomes
  - Genes from MAG: Genes from Metagenome-Assembled Genomes
  - Genes from Metagenome: Predicted genes from raw metagenome assemblies
- Configurable E-value threshold (1e-5, 1e-3, 1e-1)
- Support for both sequence input and file upload

#### Usage
1. Select BLAST method
   - blastn: For nucleotide queries against nucleotide database
   - tblastn: For protein queries against translated nucleotide database
2. Choose target database based on your research needs
3. Set E-value threshold (default: 1e-5)
4. Input sequence or upload FASTA file
   - Maximum sequence length: 50,000 bp
   - Maximum file size: 5MB
5. Submit query

#### Results
- Shows matches with:
  - Query/Subject alignments with highlighted matching regions
  - Identity percentage and coverage
  - E-value scores for match significance
  - Bit scores for comparison across searches
  - Direct links to detailed genome/gene pages
  - Downloadable alignment details

#### Common Questions
1. **Which BLAST method should I use?**
   - Use blastn for DNA/RNA sequences
   - Use tblastn for protein sequences
   - When in doubt, start with blastn for raw sequences

2. **What E-value should I choose?**
   - 1e-5 (default): Standard stringency
   - 1e-3: More permissive, good for distant homologs
   - 1e-1: Most permissive, may include false positives

3. **Why can't I find my sequence?**
   - Check sequence format (should be FASTA)
   - Verify sequence quality (no ambiguous bases)
   - Try a less stringent E-value
   - Consider using a different database

### 2. Batch Symbiont Search

#### Description
Efficiently analyze multiple taxonomic records simultaneously to identify potential symbiotic relationships from taxonomic composition data.

#### Input Methods
1. **File Upload**
   - Supported formats:
     - Kraken format: Standard Kraken2 report format
     - MetaPhlAn format: MetaPhlAn v3/v4 output
     - Krona format: Hierarchical taxonomy data
   - File size limit: 10MB
   - Encoding: UTF-8 recommended
   - Example formats provided in interface

2. **Text Input**
   - Direct paste of taxonomic composition data
   - Same format requirements as file upload
   - Useful for quick analysis of small datasets

#### Required Information
- Host Order (e.g., "Lepidoptera", "Coleoptera")
  - Must match database taxonomy
  - Case-insensitive
- Host Species (e.g., "Bombyx mori", "Drosophila melanogaster")
  - Scientific names preferred
  - Common names supported but may be less accurate
- Taxonomic composition data
  - Minimum abundance threshold: 0.01%
  - Maximum taxa limit: 1000

#### Results
- Shows potential symbionts with:
  - Symbiont name and classification
  - Record ID with links to detailed information
  - Host species and taxonomic context
  - Function description and annotations
  - Abundance percentage in sample
  - Match score (0-100)
  - Visual indicators for match types:
    - 🔵 Species-level match
    - 🟢 Order-level match
    - 🟣 Host species match

#### Scoring System
Scores are calculated based on:
- Symbiont abundance (0-50 points)
  - Linear scale based on relative abundance
  - Minimum threshold: 0.01%
- Species match bonus (+20 points)
  - Exact species name match
  - Includes strain variations
- Host match bonus
  - Order match (+10 points)
  - Species match (+20 points)
- Function richness (0-5 points)
  - Based on function description length
  - Weighted by citation count

#### Common Questions
1. **What format should I use?**
   - Kraken format for metagenome data
   - MetaPhlAn format for marker gene studies
   - Krona format for amplicon data

2. **How are matches determined?**
   - Species-level: Exact taxonomic name match
   - Genus-level: Partial name match
   - Host-level: Taxonomic hierarchy match

3. **What do the scores mean?**
   - 90-100: Very high confidence match
   - 70-89: High confidence match
   - 50-69: Moderate confidence match
   - <50: Low confidence match

### 3. Taxonomic Composition Comparison

#### Description
Compare taxonomic composition across different samples and generate intuitive stacked area charts for visualization and analysis.

#### Features
- Database sample selection with filters
- Custom data upload support
- Interactive visualizations with ECharts
- Multiple data formats support
- Comparative analysis tools

#### Data Input Options
1. **Database Samples**
   - Filter by:
     - Host species (autocomplete supported)
     - Run ID (direct search)
     - Data type (metagenome/amplicon)
   - Select multiple samples (up to 20)
   - Supports both metagenome and amplicon data

2. **Custom Data Upload**
   - Supported formats:
     - Kraken reports
     - Krona text input
   - Template files available for download
   - Drag-and-drop interface
   - Automatic format detection

#### Visualization Parameters
- Taxonomic level selection
  - Phylum
  - Class
  - Order
  - Family
  - Genus
  - Species
- Top N taxa display (1-20)
  - Adjustable via slider
  - Others grouped automatically
- Sort options:
  - By abundance (default)
  - Alphabetical
  - Custom order
- Chart customization:
  - Color schemes
  - Label positions
  - Legend placement
  - Axis scaling

#### Export Options
- SVG format
  - High-quality vector graphics
  - Suitable for publications
  - Editable in vector software
- PNG format
  - Multiple resolution options
  - Transparent background available
  - Web-ready output
- CSV format
  - Raw abundance data
  - Sample metadata
  - Taxonomic classifications

#### Common Questions
1. **How many samples can I compare?**
   - Maximum 20 samples for optimal visualization
   - Larger comparisons possible via batch processing

2. **Can I customize the visualization?**
   - Yes, through the interactive interface
   - Color schemes can be modified
   - Layout options are adjustable
   - Export in editable formats

3. **What's the best way to handle rare taxa?**
   - Use the Top N feature
   - Adjust abundance thresholds
   - Group rare taxa into "Others"

## General Tips

### Performance Optimization
- Use filters to reduce result sets
- Start with higher taxonomic levels
- Cache frequently accessed data
- Limit sample numbers in visualizations
- Use appropriate file formats

### Browser Compatibility
- Optimized for modern browsers:
  - Chrome (recommended)
  - Firefox
  - Safari
  - Edge
- Requires JavaScript enabled
- Minimum screen resolution: 1024x768
- Dark mode support

### Error Handling
1. **Empty Search Results**
   - Check spelling of scientific names
   - Try using partial terms
   - Clear filters and start over
   - Use suggested auto-complete options
   - Check for alternative taxonomic classifications

2. **Data Loading**
   - Large datasets may take time to load
   - Progress indicators show status
   - Cancel options available
   - Automatic retry for failed loads

3. **Format Errors**
   - Check file encoding (use UTF-8)
   - Verify column separators
   - Ensure proper header format
   - Remove special characters

### Best Practices
1. **Data Preparation**
   - Clean your input data
   - Remove low-quality sequences
   - Check taxonomic classifications
   - Verify abundance calculations

2. **Analysis Workflow**
   - Start with broad searches
   - Refine gradually
   - Save intermediate results
   - Document parameters used

3. **Result Interpretation**
   - Consider biological context
   - Check statistical significance
   - Validate unexpected findings
   - Compare across methods

## Troubleshooting Guide

### Common Issues and Solutions

1. **Slow Performance**
   - Clear browser cache
   - Reduce dataset size
   - Use recommended browsers
   - Check internet connection

2. **File Upload Errors**
   - Verify file format
   - Check file size limits
   - Use correct encoding
   - Try splitting large files

3. **Visualization Problems**
   - Update browser
   - Clear cache
   - Reduce sample number
   - Check screen resolution

4. **Search Issues**
   - Verify taxonomy names
   - Check spelling
   - Use autocomplete
   - Try alternative terms

## Future Features

The following features are planned for future releases:
- Export functionality enhancements
  - Additional file formats
  - Batch export options
  - Custom report generation
- User authentication system
  - Personal workspaces
  - Result history
  - Custom preferences
- Additional visualization options
  - Network diagrams
  - Phylogenetic trees
  - Heatmaps
- Batch processing improvements
  - Parallel processing
  - Progress tracking
  - Result management
- API access for programmatic analysis
  - RESTful endpoints
  - Authentication tokens
  - Rate limiting
  - Documentation

## Technical Notes

### Interface Technology
- Modern web framework
  - React components
  - Vue.js integration
  - State management
- Tailwind CSS styling
  - Responsive design
  - Custom themes
  - Dark mode support
- Accessibility features
  - ARIA labels
  - Keyboard navigation
  - Screen reader support

### Data Visualization
- ECharts library integration
  - Custom themes
  - Interactive features
  - Animation support
- Performance optimization
  - Data streaming
  - Progressive loading
  - Memory management

### Search Implementation
- Real-time search
  - Debounced queries
  - Cached results
- Smart suggestions
  - Context-aware
  - Fuzzy matching
  - Taxonomic awareness

### Performance
- Optimized data loading
  - Chunked transfers
  - Progressive rendering
- Cache management
  - Browser storage
  - Server-side caching
- Compressed transfers
  - GZIP compression
  - Binary protocols

