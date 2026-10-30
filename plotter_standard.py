import matplotlib.pyplot as plt
import csv

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

def plot_complexity(csv_file, title, output_img):
    x, y = [], []
    with open(csv_file, 'r') as file:
        for line in file:
            if "Final" in line:
                continue
            parts = line.strip().split(',')
            if len(parts) == 2:
                x.append(int(parts[0]))
                y.append(int(parts[1]))

    fig, ax = plt.subplots(figsize=(10, 5))

    # Main plot (0 to 10,000)
    ax.plot(x, y, color='blue', drawstyle='steps-post', linewidth=1.2, label='Linear Complexity')
    ax.set_title(title, fontsize=12)
    ax.set_xlabel('Sequence Length Analyzed (N)')
    ax.set_ylabel('Linear Complexity (L)')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xlim(0, 10000)
    ax.set_ylim(0, 5200)

    # Inset window placed in the upper-left area
    axins = inset_axes(ax, width="38%", height="38%", loc='upper left', borderpad=2.5)
    axins.plot(x, y, color='blue', drawstyle='steps-post', linewidth=1.5)
    
    # Zoom range showing the discrete step profile
    x1, x2 = 100, 150
    y1, y2 = min(y[x1:x2+1]) - 1, max(y[x1:x2+1]) + 1
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.grid(True, linestyle=':', alpha=0.6)
    axins.set_title('Magnified Steps (N = 100 to 150)', fontsize=9)

    # Connect the zoomed box to the main axis
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="red", alpha=0.6, linestyle='--')

    plt.savefig(output_img, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_img}")

def plot_autocorrelation(csv_file, title, output_img, color='red'):
    x, y = [], []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                x.append(int(row[0]))
                y.append(int(row[1]))

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, color=color, linewidth=0.5)
    plt.title(title)
    plt.xlabel('Shift (t)')
    plt.ylabel('Correlation (C)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(output_img)
    plt.close()
    print(f"Saved: {output_img}")

if __name__ == "__main__":
    # 1. RSA Standard Graphs
    plot_complexity('results/rsa_standard_complexity_plot.csv', 
                    'RSA Linear Complexity Profile (Standard Primes)', 
                    'results/rsa_standard_complexity_graph.png')
    
    plot_autocorrelation('results/rsa_standard_auto_plot.csv', 
                         'RSA Autocorrelation (Standard Primes)', 
                         'results/rsa_standard_auto_graph.png', 
                         color='purple')

    # 2. Micali-Schnorr Standard Graphs
    plot_complexity('results/ms_standard_complexity_plot.csv', 
                    'Micali-Schnorr Linear Complexity Profile (Standard Primes)', 
                    'results/ms_standard_complexity_graph.png')
    
    plot_autocorrelation('results/ms_standard_auto_plot.csv', 
                         'Micali-Schnorr Autocorrelation (Standard Primes)', 
                         'results/ms_standard_auto_graph.png', 
                         color='orange')