import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

def plot_ultimate_comparison():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Format: (File, Label, Color, Style, Z-order to ensure visibility)
    datasets = [
        # Seed A (Maximal Order p') - Blue
        ('results/rsa_seed_a_complexity.csv', 'RSA Seed A (Solid)', 'blue', '-', 3),
        ('results/ms_seed_a_complexity.csv', 'MS Seed A (Dashed)', 'blue', '--', 4),
        
        # Seed B (Maximal Order p') - Green
        ('results/rsa_seed_b_complexity.csv', 'RSA Seed B (Solid)', 'green', '-', 1),
        ('results/ms_seed_b_complexity.csv', 'MS Seed B (Dashed)', 'green', '--', 2),
        
        # Seed C (Degenerate Order 2) - Red
        ('results/rsa_seed_c_complexity.csv', 'RSA Seed C (Solid)', 'red', '-', 5),
        ('results/ms_seed_c_complexity.csv', 'MS Seed C (Dashed)', 'red', '--', 6)
    ]
    
    axins = inset_axes(ax, width="35%", height="35%", loc='upper left', borderpad=2)
    
    for file, label, color, style, z in datasets:
        x, y = [], []
        try:
            with open(file, 'r') as f:
                for line in f:
                    if "Final" in line: continue
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        x.append(int(parts[0]))
                        y.append(int(parts[1]))
            
            ax.plot(x, y, color=color, linestyle=style, label=label, 
                    linewidth=1.5, drawstyle='steps-post', zorder=z)
            axins.plot(x, y, color=color, linestyle=style, 
                       linewidth=2, drawstyle='steps-post', zorder=z)
            
        except FileNotFoundError:
            print(f"File not found: {file}")

    ax.set_title('Comprehensive Extraction Comparison: RSA vs. Micali-Schnorr', fontsize=12)
    ax.set_xlabel('Sequence Length Analyzed (N)')
    ax.set_ylabel('Linear Complexity (L)')
    
    # Place legend outside the plot to avoid overlapping the lines
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Inset window formatting
    axins.set_xlim(100, 150)
    axins.set_ylim(45, 80)
    axins.grid(True, linestyle=':', alpha=0.6)
    axins.set_title('Magnified Steps', fontsize=9)
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="gray", alpha=0.5, linestyle=':')

    plt.savefig('results/ultimate_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: results/ultimate_comparison.png")

if __name__ == "__main__":
    plot_ultimate_comparison()