import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv("amrfinder_chromosome_summary.csv")

# Clean sample names
df['Sample'] = df['File'].str.replace('_amrfinder.txt', '')

# Get resistance class columns
resistance_cols = [col for col in df.columns if col not in ['File', 'Sample']]

# Group by main antibiotic category
categories = {}
for col in resistance_cols:
    main_cat = col.split(' / ')[0]
    if main_cat not in categories:
        categories[main_cat] = []
    categories[main_cat].append(col)

# Calculate totals for each category per sample
category_totals = {}
for cat, cols in categories.items():
    category_totals[cat] = df[cols].sum(axis=1).values

# Calculate total resistance genes per sample
total_resistance = df[resistance_cols].sum(axis=1).values

# Sort samples by total resistance genes
sorted_indices = np.argsort(total_resistance)
sorted_samples = df['Sample'].iloc[sorted_indices].values

# Create the plot
fig, ax = plt.subplots(figsize=(15, 8))

# Define colors for each category
colors = {
    'AMINOGLYCOSIDE': '#34495E',
    'BETA-LACTAM': '#E74C3C', 
    'MACROLIDE': '#9B59B6',
    'MACROLIDE/STREPTOGRAMIN': '#8E44AD',
    'PHENICOL': '#27AE60',
    'QUINOLONE': '#3498DB',
    'SULFONAMIDE': '#F39C12',
    'TETRACYCLINE': '#E91E63',
    'BLEOMYCIN': '#8D4004',
    'QUATERNARY AMMONIUM': '#607D8B'
}

# Create stacked bars
bottom = np.zeros(len(sorted_samples))
x_pos = np.arange(len(sorted_samples))

for cat in categories.keys():
    sorted_values = [category_totals[cat][i] for i in sorted_indices]
    color = colors.get(cat, '#95A5A6')  # Default gray if color not defined
    
    ax.bar(x_pos, sorted_values, bottom=bottom, 
           label=cat, color=color, edgecolor='white', linewidth=0.3)
    bottom += sorted_values

# Customize the plot
ax.set_xlabel('Samples', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of resistance genes in chromosome', fontsize=12, fontweight='bold')
ax.set_title('Antibiotic Resistance Genes Distribution', fontsize=14, fontweight='bold')

# Set x-axis labels
ax.set_xticks(x_pos)
ax.set_xticklabels(sorted_samples, rotation=45, ha='right')

# Add legend
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)

# Add grid
ax.grid(True, alpha=0.3, axis='y')
ax.set_axisbelow(True)

# Adjust layout
plt.tight_layout()

print("=== Summary Statistics ===")
print(f"Total samples: {len(df)}")
print(f"Sample with most resistance genes: {df.loc[total_resistance.argmax(), 'Sample']} ({max(total_resistance)} genes)")
print(f"Sample with least resistance genes: {df.loc[total_resistance.argmin(), 'Sample']} ({min(total_resistance)} genes)")
print(f"Average resistance genes per sample: {np.mean(total_resistance):.1f}")

print(f"\n=== Resistance Categories ===")
for cat, cols in categories.items():
    total = sum(category_totals[cat])
    print(f"{cat}: {total} total occurrences")

# Save the plot
plt.savefig('amr_chromosome_plot.png', dpi=300, bbox_inches='tight')
print(f"\nPlot saved as: amr_chromosome_plot.png")

# Show the plot
plt.show()