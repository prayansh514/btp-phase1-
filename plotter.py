import matplotlib.pyplot as plt
import csv

def plot_complexity():
    x, y = [], []
    with open('results/lfsr_complexity_plot.csv', 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Skip the final "Final Linear Complexity" text if it's at the bottom
            if "Final" in line:
                continue
            parts = line.strip().split(',')
            if len(parts) == 2:
                x.append(int(parts[0]))
                y.append(int(parts[1]))

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, color='blue', drawstyle='steps-post')
    plt.title('LFSR Linear Complexity Profile')
    plt.xlabel('Sequence Length Analyzed (N)')
    plt.ylabel('Linear Complexity (L)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0, 50) # Zooms the X-axis in to show the first 50 bits
    plt.savefig('results/lfsr_complexity_graph.png')
    plt.close()
    print("Saved: results/lfsr_complexity_graph.png")

def plot_autocorrelation():
    x, y = [], []
    with open('results/lfsr_auto_plot.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                x.append(int(row[0]))
                y.append(int(row[1]))

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, color='red', linewidth=0.5)
    plt.title('LFSR Autocorrelation')
    plt.xlabel('Shift (t)')
    plt.ylabel('Correlation (C)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('results/lfsr_auto_graph.png')
    plt.close()
    print("Saved: results/lfsr_auto_graph.png")

if __name__ == "__main__":
    plot_complexity()
    plot_autocorrelation()