import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv('11chung_RS.csv')

# Clean the data - remove empty columns and rows
df = df.dropna(axis=1, how='all')  # Remove completely empty columns
df = df.dropna(axis=0, how='all')  # Remove completely empty rows

# Get the actual data starting from row with antibiotic abbreviations
# Find the row that contains the antibiotic abbreviations
antibiotic_row = None
for i, row in df.iterrows():
    if 'CIP' in str(row.values):
        antibiotic_row = i
        break

if antibiotic_row is not None:
    # Extract column names (antibiotic abbreviations)
    antibiotics = df.iloc[antibiotic_row, 2:].values  # Skip 'No' and 'Commn Name' columns
    antibiotics = [ab for ab in antibiotics if pd.notna(ab) and ab != '']
    
    # Extract bacterial strain names and resistance data
    data_rows = df.iloc[antibiotic_row+1:].copy()
    data_rows = data_rows.dropna(subset=[df.columns[1]])  # Remove rows without strain names
    
    # Extract strain names (remove numbering if present)
    strain_names = data_rows.iloc[:, 1].values
    
    # Extract resistance data
    resistance_data = data_rows.iloc[:, 2:2+len(antibiotics)].values
    
    # Convert R/I/S to numerical values
    # R (Resistant) = 2, I (Intermediate) = 1, S (Sensitive) = 0
    resistance_matrix = np.zeros((len(strain_names), len(antibiotics)))
    
    for i in range(len(strain_names)):
        for j in range(len(antibiotics)):
            if j < resistance_data.shape[1]:
                val = str(resistance_data[i, j]).strip().upper()
                if val == 'R':
                    resistance_matrix[i, j] = 2
                elif val == 'I':
                    resistance_matrix[i, j] = 1
                elif val == 'S':
                    resistance_matrix[i, j] = 0
                else:
                    resistance_matrix[i, j] = np.nan
    
    # Create DataFrame for heatmap
    heatmap_df = pd.DataFrame(resistance_matrix, 
                             index=strain_names, 
                             columns=antibiotics)
    
    # Create the heatmap
    plt.figure(figsize=(16, 10))
    
    # Custom colormap: Green for Sensitive, White for Intermediate, Red for Resistant
    colors = ['#00A651', '#FFFFFF', '#E74C3C']  # Green, White, Red
    n_bins = 3
    cmap = plt.cm.colors.ListedColormap(colors)
    
    # Create heatmap
    sns.heatmap(heatmap_df, 
                cmap=cmap, 
                vmin=0, 
                vmax=2,
                cbar_kws={'ticks': [0, 1, 2], 
                         'label': 'Resistance Level'},
                linewidths=0.5,
                linecolor='white',
                square=False,
                annot=False)
    
    # Customize the plot
    plt.title('Antibiotic Resistance Patterns Heatmap', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Antibiotics', fontsize=12, fontweight='bold')
    plt.ylabel('Bacterial Strains', fontsize=12, fontweight='bold')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Customize colorbar
    cbar = plt.gca().collections[0].colorbar
    cbar.set_ticklabels(['Susceptible(S)', 'Intermediate (I)', 'Resistant (R)'])
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Show the plot
    plt.show()
    
    #plt.savefig("RIS_11chung.png", dpi  =300)