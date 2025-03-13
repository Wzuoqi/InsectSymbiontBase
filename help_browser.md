# InsectSymbiontDB Data Browser: User Guide

## 1. Overview

The InsectSymbiontDB Data Browser is a comprehensive interface for exploring insect-symbiont relationships. It consists of four main sections:

- **Symbiont Records**: A database of verified functional symbionts from scientific literature, focusing on functional relationships between insects and their microbial partners
- **Insect Hosts**: A taxonomic browser for host species and their associated symbionts, organized in a hierarchical structure
- **Metagenomes**: Collection of insect-associated metagenome samples with detailed metadata and analysis results
- **Amplicons**: Repository of amplicon sequencing data from insect microbiome studies, including 16S rRNA and ITS sequences

Current database statistics:
- 2,657+ functional symbiont records
  - 2,130 bacterial symbionts
  - 253 fungal symbionts
  - 230 other symbionts
- 1,494+ metagenome samples across 6 continents
  - 387 from Europe
  - 310 from South America
  - 308 from Asia
  - 265 from North America
  - 80 from Africa
  - 8 from Oceania
- 14,992+ amplicon samples
  - 8,900 16S rRNA sequences
  - 1,318 ITS sequences
  - 98 other sequences
- 1,000+ insect host species across multiple orders
  - 333 Hemiptera species
  - 254 Coleoptera species
  - 147 Hymenoptera species
  - 121 Lepidoptera species
  - 118 Diptera species
  - 92 Blattodea species
  - 54 other species

## 2. Access and Navigation

### 2.1 Main Navigation

The database can be accessed through four main entry points from the homepage:

1. **Symbiont Record**:
   - Browse verified symbiont functions from literature
   - Access comprehensive functional annotations
   - View symbiont-host relationships
   - Explore function classifications

2. **Insect Host**:
   - Navigate through taxonomic hierarchy
   - Access species-specific information
   - View associated symbionts
   - Explore host-symbiont networks

3. **Metagenome**:
   - Browse metagenome sequencing data
   - Access assembly and analysis results
   - View taxonomic compositions
   - Download processed data

4. **Amplicon**:
   - Access amplicon sequencing records
   - View taxonomic classifications
   - Explore microbial diversity
   - Compare community structures

### 2.2 Interface Layout

Each section features a consistent layout with:
- Top navigation bar
- Search interface
- Main content area
- Interactive visualizations
- Floating home button (bottom-right)
- Advanced search toggle
- Filter reset options

## 3. Search Features

### 3.1 Basic Search

Each data browser section includes a basic search bar that supports:
- Keyword search across all fields
- Real-time search suggestions
- Auto-completion for species names, functions, and taxonomic terms

Search tips:
- Use scientific names for most accurate results
- Partial name searches are supported
- Case-insensitive searching
- Special characters are handled automatically

### 3.2 Advanced Search

#### Symbiont Records Advanced Search
Fields include:
- Host Information
  - Order (e.g., "Lepidoptera", "Coleoptera")
  - Family (e.g., "Noctuidae", "Cerambycidae")
  - Species (e.g., "Spodoptera frugiperda")
- Symbiont Information
  - Name (e.g., "Wolbachia", "Metarhizium")
  - Phylum (e.g., "Proteobacteria", "Ascomycota")
  - Order (e.g., "Rickettsiales", "Hypocreales")
  - Genus (e.g., "Bacillus", "Beauveria")
- Function Information
  - Classification (e.g., "Nutrition", "Defense")
  - Function Tags (e.g., "N-fixation", "Antimicrobial")
- Genome ID (e.g., "GCA_000789775.1")

#### Metagenome Advanced Search
Fields include:
- Run Number (e.g., "SRR12345678")
- Assay Type (e.g., "WGS", "RNA-Seq")
- BioSample/BioProject (e.g., "PRJNA123456")
- Geographic Location
  - Country
  - Continent
  - Specific location
- Host Species
- Environmental Information
  - Collection site
  - Sample type
  - Environmental conditions

#### Amplicon Advanced Search
Fields include:
- Run Number
- Assay Type (e.g., "16S", "ITS")
- Classification
  - 16S rRNA
  - ITS
  - Others
- Geographic Location
  - Country
  - Continent
  - Specific location
- Host Information
  - Species
  - Life stage
  - Sex
- Environmental Parameters
  - Collection site
  - Sample type
  - Environmental conditions

## 4. Data Display & Interpretation

### 4.1 Symbiont Records View
Displays:
- Symbiont name and phylum
  - Color-coded by classification
  - Links to detailed pages
- Host insect species and order
  - Links to host information
  - Taxonomic context
- Classification
  - Bacteria/Fungi/Others
  - Visual indicators
- Function description
  - Detailed annotations
  - Literature context
- Function tags (color-coded)
  - Nutrition-related (green)
  - Defense-related (orange)
  - Physiology-related (purple)
- Publication year
- DOI links to original research

### 4.2 Metagenome View
Shows:
- Run number (with direct links)
- Host species (linked to taxonomy)
- Bioproject ID (with external links)
- Sequencing type
  - Platform information
  - Library details
- Geographic location
  - Country and continent
  - Specific coordinates when available
- Collection year
- Additional metadata
  - Environmental information
  - Sample processing details

### 4.3 Amplicon View
Presents:
- Run ID (with links)
- Assay type
  - 16S rRNA
  - ITS
  - Other markers
- Classification
  - Taxonomic assignments
  - Confidence scores
- Host species
- Geographic area
- Environmental information
  - Collection site details
  - Sample type
  - Processing methods
- Collection year

### 4.4 Host Browser View
Organized as an interactive taxonomic tree with:
- Order level
  - Major insect orders
  - Species counts
  - Distribution information
- Family level
  - Taxonomic groupings
  - Related species
- Genus level
  - Species lists
  - Common characteristics
- Species level
  - Detailed information
  - Associated symbionts
  - Available data types

## 5. Filtering & Refinement

### 5.1 Filter Types
- **Symbiont Records**
  - By classification (Bacteria/Fungi)
  - By function category
  - By host taxonomy
  - By publication year

- **Metagenomes**
  - By sequencing platform
  - By geographic region
  - By host species
  - By data size
  - By completion status

- **Amplicons**
  - By marker type (16S/ITS/Other)
  - By geographic region
  - By host taxonomy
  - By environmental parameters

- **Hosts**
  - By taxonomic rank
  - By geographic distribution
  - By symbiont association
  - By data availability

### 5.2 Data Visualization
Each section includes relevant charts:

#### Symbiont Distribution
- Pie charts showing:
  - Bacterial vs. fungal symbionts
  - Function category distribution
  - Host order distribution

#### Geographic Distribution
- World map visualization
- Continental distribution charts
- Sample density heatmaps

#### Taxonomic Distribution
- Interactive trees
- Order-level distribution charts
- Species abundance plots

#### Function Analysis
- Function category sunburst charts
- Tag co-occurrence networks
- Temporal distribution plots

## 6. Known Issues & FAQs

### Common Scenarios
1. **Empty Search Results**:
   - Check spelling of scientific names
   - Try using partial terms
   - Clear filters and start over
   - Use suggested auto-complete options
   - Check for alternative taxonomic classifications

2. **Navigation**:
   - Use breadcrumbs for hierarchy navigation
   - Home button available in bottom-right corner
   - Reset button to clear all filters
   - Browser back button supported
   - Bookmark support for specific views

3. **Data Loading**:
   - Large datasets may take time to load
   - Charts render progressively
   - Use filters to reduce result set
   - Cache frequently accessed data

4. **Browser Compatibility**:
   - Optimized for modern browsers
   - Requires JavaScript enabled
   - Supports responsive layouts
   - Dark mode detection

## 7. Additional Features

### 7.1 Interactive Elements
- Hoverable cards with additional information
  - Preview of detailed data
  - Quick access to related records
  - Context-sensitive actions
- Expandable taxonomic trees
  - Multi-level navigation
  - Collapsible sections
  - Search within tree
- Clickable function tags
  - Filter by function
  - View related records
  - Function definitions
- Direct links to literature references
  - DOI integration
  - PubMed links
  - Citation information

### 7.2 Data Visualization
- Interactive charts using ECharts
  - Zoom and pan support
  - Data point selection
  - Custom view options
  - Export capabilities
- Responsive design
  - Mobile-friendly layouts
  - Touch interaction support
  - Adaptive charts
- Dark mode support
  - Automatic detection
  - Manual toggle
  - Preserved user preference

## 8. Technical Notes

### 8.1 Interface Technology
- Modern web framework
  - Tailwind CSS for styling
  - Responsive grid system
  - Custom components
  - Accessibility features

### 8.2 Data Visualization
- ECharts library integration
  - Custom themes
  - Responsive charts
  - Interactive features
  - Performance optimization

### 8.3 Search Implementation
- Real-time search
  - Debounced queries
  - Cached results
  - Smart suggestions
  - Error handling

### 8.4 Performance
- Optimized data loading
  - Progressive rendering
  - Lazy loading
  - Cache management
  - Compressed transfers

Note: Export functionality and user authentication features are planned for future releases. The current documentation reflects the implemented features visible in the templates.
