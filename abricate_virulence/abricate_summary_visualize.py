import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Configuration - Change these paths as needed
CSV_FILE = "Gene_Presence_Absence_Matrix.csv"
OUTPUT_FILE = "gene_visualization.png"

def visualize_gene_matrix():
    """
    Create visualization of gene presence/absence matrix
    """
    
    # Read the CSV file
    try:
        df = pd.read_csv(CSV_FILE, index_col=0)
        print(f"Loaded matrix with {df.shape[0]} samples and {df.shape[1]} genes")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Clean sample names (remove file extensions)
    df.index = [name.replace('_vfdb.csv', '').replace('ERR', '') for name in df.index]
    
    # Calculate gene counts per sample
    gene_counts = df.sum(axis=1).sort_values(ascending=True)
    
    # Define gene categories based on prefixes/patterns
    categories = {
        'Adhesion & Biofilm': ['ata', 'bap', 'csu', 'fim', 'pil', 'ompA', 'pga'],
        'Secretion Systems': ['gsp', 'tss', 'hcp', 'vgrG', 'clpV'],
        'LPS & Cell Wall': ['lpx', 'lps', 'galE', 'galU', 'pbpG'],
        'Virulence Regulation': ['aba', 'ade', 'bar', 'bas', 'bau', 'bfm'],
        'Phospholipases': ['plc'],
        'Iron Acquisition': ['bas', 'bau', 'entE'],
        'Other Virulence': []
    }
    
    # Color palette
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    # Assign genes to categories
    gene_categories = {}
    assigned_genes = set()
    
    for category, prefixes in categories.items():
        for gene in df.columns:
            for prefix in prefixes:
                if gene.lower().startswith(prefix.lower()) or prefix.lower() in gene.lower():
                    gene_categories[gene] = category
                    assigned_genes.add(gene)
                    break
    
    # Assign remaining genes to 'Other Virulence'
    for gene in df.columns:
        if gene not in assigned_genes:
            gene_categories[gene] = 'Other Virulence'
    
    # Create figure with single plot
    fig, ax1 = plt.subplots(1, 1, figsize=(12, 10))
    
    # --- PLOT 1: Stacked Bar Chart ---
    sample_names = gene_counts.index
    y_positions = np.arange(len(sample_names))
    
    # Calculate category counts for each sample
    unique_categories = list(set(gene_categories.values()))
    category_data = {}
    category_colors = {}
    
    for i, category in enumerate(unique_categories):
        category_genes = [gene for gene, cat in gene_categories.items() if cat == category]
        category_data[category] = df[category_genes].sum(axis=1)[sample_names]
        category_colors[category] = colors[i % len(colors)]
    
    # Create stacked horizontal bar chart
    left_positions = np.zeros(len(sample_names))
    
    for category in unique_categories:
        if category_data[category].sum() > 0:
            ax1.barh(y_positions, category_data[category],
                    left=left_positions,
                    color=category_colors[category],
                    label=category,
                    height=0.8)
            left_positions += category_data[category]
    
    # Customize stacked bar chart
    ax1.set_yticks(y_positions)
    ax1.set_yticklabels(sample_names)
    ax1.set_xlabel('Number of Virulence Genes')
    ax1.set_ylabel('Samples')
    ax1.set_title('Virulence Gene Distribution by Category', fontweight='bold')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add total counts
    for i, count in enumerate(gene_counts):
        ax1.text(count + 1, i, str(count),
                va='center', ha='left', fontsize=8, fontweight='bold')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure as PNG
    try:
        plt.savefig(OUTPUT_FILE, 
                   dpi=300,           # High resolution
                   bbox_inches='tight', # Remove extra whitespace
                   facecolor='white',   # White background
                   edgecolor='none')    # No border
        print(f"Visualization saved as: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error saving PNG file: {e}")
    
    # Display the plot
    plt.show()
    
    # Print summary statistics
    print(f"\nSummary Statistics:")
    print(f"Total samples: {len(df)}")
    print(f"Total genes: {len(df.columns)}")
    print(f"Average genes per sample: {gene_counts.mean():.1f}")
    print(f"Sample with most genes: {gene_counts.idxmax()} ({gene_counts.max()} genes)")
    print(f"Sample with least genes: {gene_counts.idxmin()} ({gene_counts.min()} genes)")
    
    # Category summary
    print(f"\nGenes per category:")
    for category in unique_categories:
        count = sum(1 for cat in gene_categories.values() if cat == category)
        print(f"  {category}: {count} genes")

# Run the visualization
if __name__ == "__main__":
    visualize_gene_matrix()
    