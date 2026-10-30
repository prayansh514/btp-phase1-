import numpy as np
import matplotlib.pyplot as plt

files = {
    'Standard': ('results/rsa_standard_complexity_plot.csv', 'results/rsa_standard_auto_plot.csv'),
    'Safe': ('results/rsa_safe_complexity_plot.csv', 'results/rsa_safe_auto_plot.csv'),
    'Sophie Germain': ('results/rsa_sophie_complexity_plot.csv', 'results/rsa_sophie_auto_plot.csv')
}

print(f"{'Prime Type':<16} | {'Final L':<8} | {'Max |C(t)| (t>0)':<18} | {'Auto Variance':<14} | {'BM Steps (Jumps)':<16}")
print("-" * 80)

plt.figure(figsize=(10, 5))

for label, (comp_csv, auto_csv) in files.items():
    # 1. Parse Complexity CSV
    n_vals, l_vals = [], []
    with open(comp_csv, 'r') as f:
        for line in f:
            if "Final" in line: continue
            parts = line.strip().split(',')
            if len(parts) == 2:
                n_vals.append(int(parts[0]))
                l_vals.append(int(parts[1]))

    n_arr = np.array(n_vals)
    l_arr = np.array(l_vals)

    final_l = l_arr[-1]
    # Count how many times Berlekamp-Massey had to update L
    bm_jumps = np.count_nonzero(np.diff(l_arr) > 0)
    
    # Deviation from ideal random expectation (N/2)
    deviation = l_arr - (n_arr / 2.0)

    # 2. Parse Autocorrelation CSV
    auto_c = []
    with open(auto_csv, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 2:
                auto_c.append(int(parts[1]))
    
    # Discard C(0) for sidelobe statistics
    sidelobes = np.array(auto_c[1:])
    max_sidelobe = np.max(np.abs(sidelobes))
    auto_var = np.var(sidelobes)

    print(f"{label:<16} | {final_l:<8} | {max_sidelobe:<18} | {auto_var:<14.2f} | {bm_jumps:<16}")

    # Plot deviation profile
    plt.plot(n_arr, deviation, label=f"{label} Prime", linewidth=0.8)

plt.title('Linear Complexity Deviation Profile: $L(N) - N/2$')
plt.xlabel('Sequence Length (N)')
plt.ylabel('Deviation from $N/2$')
plt.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.7)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.savefig('results/prime_comparison_deviation.png', dpi=300, bbox_inches='tight')
plt.close()
print("\nSaved deviation plot: results/prime_comparison_deviation.png")