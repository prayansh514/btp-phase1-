import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

def plot_order_experiment_with_inset(csv_a, csv_b, csv_c, title, output_img):
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Define files and their plot styles
    datasets = [
        (csv_a, 'Seed A: Quadratic Residue (Order p\')', 'blue', '-'),    # Solid blue
        (csv_b, 'Seed B: Quadratic Residue (Order p\')', 'green', '--'),  # Dashed green to show overlap
        (csv_c, 'Seed C: Trivial Non-Residue (Order 2)', 'red', '-')      # Solid red
    ]
    
    # Inset axis setup
    axins = inset_axes(ax, width="35%", height="35%", loc='upper left', borderpad=2)
    
    for file, label, color, style in datasets:
        x, y = [], []
        try:
            with open(file, 'r') as f:
                for line in f:
                    if "Final" in line: continue
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        x.append(int(parts[0]))
                        y.append(int(parts[1]))
            
            # Plot on main axis
            ax.plot(x, y, color=color, linestyle=style, label=label, linewidth=1.5, drawstyle='steps-post')
            
            # Plot on inset axis
            axins.plot(x, y, color=color, linestyle=style, linewidth=2, drawstyle='steps-post')
            
        except FileNotFoundError:
            print(f"File not found: {file}")

    # Main plot formatting
    ax.set_title(title, fontsize=12)
    ax.set_xlabel('Sequence Length Analyzed (N)')
    ax.set_ylabel('Linear Complexity (L)')
    ax.legend(loc='lower right')
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Inset window formatting (Zooming in on N=100 to N=150)
    x1, x2 = 100, 150
    y1, y2 = 45, 80 
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.grid(True, linestyle=':', alpha=0.6)
    axins.set_title('Magnified Steps', fontsize=9)
    
    # Connect inset to main plot
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="gray", alpha=0.5, linestyle=':')

    plt.savefig(output_img, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_img}")

if __name__ == "__main__":
    plot_order_experiment_with_inset(
        'results/rsa_seed_a_complexity.csv',
        'results/rsa_seed_b_complexity.csv',
        'results/rsa_seed_c_complexity.csv',
        'RSA Generator: Linear Complexity vs. Algebraic Order (Safe Prime)',
        'results/rsa_order_vs_complexity.png'
    )
    
    plot_order_experiment_with_inset(
        'results/ms_seed_a_complexity.csv',
        'results/ms_seed_b_complexity.csv',
        'results/ms_seed_c_complexity.csv',
        'Micali-Schnorr Generator: Linear Complexity vs. Algebraic Order (Safe Prime)',
        'results/ms_order_vs_complexity.png'
    )