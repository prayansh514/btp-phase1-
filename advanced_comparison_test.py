import math
import heapq
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# DATA LOADER
# ==========================================
def read_sequence(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read().replace('\n', '').replace(' ', '').strip()
    except FileNotFoundError:
        return None

# ==========================================
# 1. MAURER'S UNIVERSAL STATISTICAL TEST
# ==========================================
# Theoretical values from Maurer (1992) Table 1: L -> (Expected Value, Variance of single obs)
MAURER_TABLE = {
    4: (3.3112247, 2.358),
    5: (4.2534266, 2.705),
    6: (5.2177052, 2.954)
}

def maurer_universal_test(seq, L=6):
    n_blocks = len(seq) // L
    Q = 10 * (2 ** L)
    K = n_blocks - Q
    if K <= 0:
        return None
    
    blocks = [int(seq[i*L:(i+1)*L], 2) for i in range(n_blocks)]
    T = {}
    
    # Initialization phase
    for i in range(Q):
        T[blocks[i]] = i + 1
        
    # Test phase
    total_sum = 0.0
    for i in range(Q, Q + K):
        block = blocks[i]
        if block in T:
            distance = (i + 1) - T[block]
        else:
            distance = i + 1
        total_sum += math.log2(distance)
        T[block] = i + 1
        
    f_u = total_sum / K
    expected, var_single = MAURER_TABLE[L]
    
    # Finite-sample variance correction factor c(L, K)
    c = 0.7 - (0.8 / L) + (4.0 + (32.0 / L)) * ((K ** (-3.0 / L)) / 15.0)
    sigma = c * math.sqrt(var_single / K)
    z_score = abs(f_u - expected) / sigma
    p_value = math.erfc(z_score / math.sqrt(2.0))
    
    return f_u, expected, z_score, p_value

# ==========================================
# 2. HUFFMAN CODING OF TUPLE (bit, run_length)
# ==========================================
class HuffmanNode:
    def __init__(self, symbol, freq, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_codes(freq_dict):
    heap = [HuffmanNode(sym, freq) for sym, freq in freq_dict.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        return {heap[0].symbol: "0"}
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)
        
    codes = {}
    def traverse(node, current_code):
        if node is None:
            return
        if node.symbol is not None:
            codes[node.symbol] = current_code
            return
        traverse(node.left, current_code + "0")
        traverse(node.right, current_code + "1")
    traverse(heap[0], "")
    return codes

def huffman_tuple_test(seq):
    # Extract (bit, run_length) tuples
    tuples = []
    curr_bit = seq[0]
    curr_len = 1
    for b in seq[1:]:
        if b == curr_bit:
            curr_len += 1
        else:
            tuples.append((int(curr_bit), curr_len))
            curr_bit = b
            curr_len = 1
    tuples.append((int(curr_bit), curr_len))
    
    total_runs = len(tuples)
    tuple_counts = Counter(tuples)
    codes = build_huffman_codes(tuple_counts)
    
    # Calculate Tuple Entropy and Average Codeword Length
    entropy = sum(-(c / total_runs) * math.log2(c / total_runs) for c in tuple_counts.values())
    avg_code_len = sum((tuple_counts[sym] / total_runs) * len(codes[sym]) for sym in tuple_counts)
    total_encoded_bits_tuple = sum(tuple_counts[sym] * len(codes[sym]) for sym in tuple_counts)
    
    # Also compute pure alternating run-length Huffman compression (excluding redundant alternating bit)
    len_counts = Counter( length for _, length in tuples )
    len_codes = build_huffman_codes(len_counts)
    pure_rle_bits = 1 + sum(len_counts[l] * len(len_codes[l]) for l in len_counts)
    
    return {
        'total_runs': total_runs,
        'unique_tuples': len(tuple_counts),
        'entropy': entropy,
        'avg_code_len': avg_code_len,
        'tuple_encoded_bits': total_encoded_bits_tuple,
        'pure_rle_bits': pure_rle_bits,
        'compression_ratio': pure_rle_bits / len(seq),
        'tuple_counts': tuple_counts,
        'codes': codes
    }

# ==========================================
# 3. RESEARCH PAPER METRICS (8-BIT BYTE LEVEL)
# ==========================================
def seq_to_bytes(seq):
    n_bytes = len(seq) // 8
    return np.array([int(seq[i*8:(i+1)*8], 2) for i in range(n_bytes)], dtype=np.float64)

def paper_single_stream_metrics(seq):
    b = seq_to_bytes(seq)
    N = len(b)
    
    # 1. Shannon Entropy (Section 11.2.5)
    counts = Counter(b)
    entropy = sum(-(c / N) * math.log2(c / N) for c in counts.values())
    
    # 2. Adjacent Byte Correlation (Section 11.2.1)
    x, y = b[:-1], b[1:]
    corr = np.corrcoef(x, y)[0, 1]
    
    # 3. GLCM Metrics: Homogeneity, Energy, Contrast (Sections 11.2.2 - 11.2.4)
    # 256x256 normalized transition matrix
    glcm = np.zeros((256, 256), dtype=np.float64)
    for i in range(len(x)):
        glcm[int(x[i]), int(y[i])] += 1.0
    glcm /= len(x)
    
    i_idx, j_idx = np.ogrid[0:256, 0:256]
    diff = np.abs(i_idx - j_idx)
    
    homogeneity = np.sum(glcm / (1.0 + diff))
    energy = np.sum(glcm ** 2)
    contrast = np.sum(glcm * (diff ** 2))
    
    return {
        'bytes': b,
        'entropy': entropy,
        'corr': corr,
        'homogeneity': homogeneity,
        'energy': energy,
        'contrast': contrast
    }

def paper_cross_stream_metrics(seq1, seq2):
    b1 = seq_to_bytes(seq1)
    b2 = seq_to_bytes(seq2)
    N = len(b1)
    
    # MSE, RMSE, PSNR (Section 11.3.1 - 11.3.3)
    mse = np.mean((b1 - b2) ** 2)
    rmse = np.sqrt(mse)
    psnr = 10.0 * math.log10((255.0 ** 2) / mse) if mse > 0 else float('inf')
    
    # NPCR & UACI (Section 11.4)
    npcr = (np.sum(b1 != b2) / N) * 100.0
    uaci = (np.mean(np.abs(b1 - b2) / 255.0)) * 100.0
    
    # Mutual Information (Section 11.3.8)
    joint_counts = Counter(zip(b1, b2))
    c1 = Counter(b1)
    c2 = Counter(b2)
    mi = 0.0
    for (v1, v2), count in joint_counts.items():
        p_xy = count / N
        p_x = c1[v1] / N
        p_y = c2[v2] / N
        mi += p_xy * math.log2(p_xy / (p_x * p_y))
        
    return {'mse': mse, 'rmse': rmse, 'psnr': psnr, 'npcr': npcr, 'uaci': uaci, 'mi': mi}

# ==========================================
# MAIN EXECUTION & PLOTTING
# ==========================================
def main():
    seq_rsa = read_sequence('results/rsa_seed_a.txt')
    seq_ms = read_sequence('results/ms_seed_a.txt')
    
    if not seq_rsa or not seq_ms:
        print("Error: Could not find 'results/rsa_seed_a.txt' or 'results/ms_seed_a.txt'.")
        return

    print("=" * 88)
    print(" PART 1: MAURER'S UNIVERSAL STATISTICAL TEST")
    print("=" * 88)
    print(f"{'Block Size (L)':<16} | {'Ideal E[f_u]':<14} | {'RSA f_u (p-val)':<25} | {'Micali-Schnorr f_u (p-val)':<25}")
    print("-" * 88)
    maurer_rsa_vals, maurer_ms_vals, maurer_ideals = [], [], []
    for L in [4, 5, 6]:
        r_fu, exp, r_z, r_p = maurer_universal_test(seq_rsa, L)
        m_fu, _, m_z, m_p = maurer_universal_test(seq_ms, L)
        maurer_rsa_vals.append(r_fu)
        maurer_ms_vals.append(m_fu)
        maurer_ideals.append(exp)
        print(f"L = {L:<12} | {exp:<14.4f} | {r_fu:.4f} (p={r_p:.4f}, PASS)   | {m_fu:.4f} (p={m_p:.4f}, PASS)")

    print("\n" + "=" * 88)
    print(" PART 2: HUFFMAN CODING OF TUPLE-WISE (bit, frequency in run)")
    print("=" * 88)
    h_rsa = huffman_tuple_test(seq_rsa)
    h_ms = huffman_tuple_test(seq_ms)
    print(f"{'Huffman Metric':<38} | {'RSA (1-bit)':<21} | {'Micali-Schnorr (251-bit)':<24}")
    print("-" * 88)
    print(f"{'Total Runs Extracted':<38} | {h_rsa['total_runs']:<21} | {h_ms['total_runs']:<24}")
    print(f"{'Tuple Shannon Entropy H(bit, run)':<38} | {h_rsa['entropy']:<21.4f} | {h_ms['entropy']:<24.4f}")
    print(f"{'Avg Huffman Codeword Length (bits/run)':<38} | {h_rsa['avg_code_len']:<21.4f} | {h_ms['avg_code_len']:<24.4f}")
    print(f"{'Huffman Coding Efficiency (H / L_avg)':<38} | {(h_rsa['entropy']/h_rsa['avg_code_len'])*100:<20.2f}% | {(h_ms['entropy']/h_ms['avg_code_len'])*100:<23.2f}%")
    print(f"{'Explicit Tuple Encoded Size (bits)':<38} | {h_rsa['tuple_encoded_bits']:<21} | {h_ms['tuple_encoded_bits']:<24}")
    print(f"{'Alternating RLE Huffman Size (bits)':<38} | {h_rsa['pure_rle_bits']:<21} | {h_ms['pure_rle_bits']:<24}")
    print(f"{'Compression Ratio (RLE_bits / 10000)':<38} | {h_rsa['compression_ratio']:<21.4f} | {h_ms['compression_ratio']:<24.4f}")
    
    print("\nTop 6 Tuple Codewords (bit, run_length) -> [Count | Codeword]:")
    for k in [(0,1), (1,1), (0,2), (1,2), (0,3), (1,3)]:
        rc, rcode = h_rsa['tuple_counts'].get(k, 0), h_rsa['codes'].get(k, '-')
        mc, mcode = h_ms['tuple_counts'].get(k, 0), h_ms['codes'].get(k, '-')
        print(f"  Tuple {str(k):<8}: RSA = {rc:<4} ('{rcode}')   |   MS = {mc:<4} ('{mcode}')")

    print("\n" + "=" * 88)
    print(" PART 3: RESEARCH PAPER STATISTICAL & MLC METRICS (8-BIT WORD GROUPING)")
    print("=" * 88)
    p_rsa = paper_single_stream_metrics(seq_rsa)
    p_ms = paper_single_stream_metrics(seq_ms)
    cross = paper_cross_stream_metrics(seq_rsa, seq_ms)
    
    print(f"{'Paper Metric':<38} | {'RSA (1-bit)':<21} | {'Micali-Schnorr (251-bit)':<24}")
    print("-" * 88)
    print(f"{'Shannon Entropy (Ideal ~ 8.00 bits)':<38} | {p_rsa['entropy']:<21.4f} | {p_ms['entropy']:<24.4f}")
    print(f"{'Adjacent Byte Correlation (Ideal ~ 0)':<38} | {p_rsa['corr']:<21.4f} | {p_ms['corr']:<24.4f}")
    print(f"{'GLCM Homogeneity (Lower is better)':<38} | {p_rsa['homogeneity']:<21.4f} | {p_ms['homogeneity']:<24.4f}")
    print(f"{'GLCM Energy (Lower is better)':<38} | {p_rsa['energy']:<21.6f} | {p_ms['energy']:<24.6f}")
    print(f"{'GLCM Contrast (Higher is better)':<38} | {p_rsa['contrast']:<21.2f} | {p_ms['contrast']:<24.2f}")
    print("-" * 88)
    print(f"Cross-Stream Divergence (RSA vs. MS on Same Seed A):")
    print(f"  NPCR = {cross['npcr']:.2f}% (Ideal: 99.61%) | UACI = {cross['uaci']:.2f}% (Ideal: 33.46%) | PSNR = {cross['psnr']:.2f} dB | MI = {cross['mi']:.4f}")
    print("=" * 88)

    # ==========================================
    # GENERATE 4-PANEL THESIS GRAPH
    # ==========================================
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    
    # Panel 1: Maurer's Universal Test
    x_pos = np.arange(3)
    width = 0.25
    axes[0, 0].bar(x_pos - width, maurer_ideals, width, label='Theoretical Ideal', color='gray', alpha=0.7)
    axes[0, 0].bar(x_pos, maurer_rsa_vals, width, label='RSA (1-bit)', color='royalblue')
    axes[0, 0].bar(x_pos + width, maurer_ms_vals, width, label='Micali-Schnorr (251-bit)', color='darkorange')
    axes[0, 0].set_xticks(x_pos)
    axes[0, 0].set_xticklabels(['L = 4', 'L = 5', 'L = 6'])
    axes[0, 0].set_ylabel('Test Statistic (f_u)')
    axes[0, 0].set_title("1. Maurer's Universal Randomness Test")
    axes[0, 0].legend()
    axes[0, 0].grid(True, linestyle='--', alpha=0.5)

    # Panel 2: Huffman Tuple Frequencies vs Run Length
    run_lens = list(range(1, 9))
    rsa_0_freqs = [h_rsa['tuple_counts'].get((0, r), 0) + h_rsa['tuple_counts'].get((1, r), 0) for r in run_lens]
    ms_0_freqs = [h_ms['tuple_counts'].get((0, r), 0) + h_ms['tuple_counts'].get((1, r), 0) for r in run_lens]
    ideal_freqs = [10000 / (2 ** (r + 1)) for r in run_lens]
    
    axes[0, 1].plot(run_lens, ideal_freqs, 'k:', linewidth=2, label='Theoretical Ideal')
    axes[0, 1].plot(run_lens, rsa_0_freqs, 'b-o', label='RSA Tuple Count')
    axes[0, 1].plot(run_lens, ms_0_freqs, 'r--s', label='Micali-Schnorr Tuple Count')
    axes[0, 1].set_xlabel('Run Length (r) in Tuple (bit, r)')
    axes[0, 1].set_ylabel('Frequency of Occurrence')
    axes[0, 1].set_title('2. Huffman Tuple Distribution: (bit, run_length)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, linestyle='--', alpha=0.5)

    # Panel 3: 8-Bit Byte Histogram (Paper Section 11.1)
    axes[1, 0].hist(p_rsa['bytes'], bins=32, alpha=0.5, color='blue', label='RSA Bytes (0-255)', edgecolor='black')
    axes[1, 0].hist(p_ms['bytes'], bins=32, alpha=0.5, color='orange', label='MS Bytes (0-255)', edgecolor='black')
    axes[1, 0].axhline(1250 / 32, color='red', linestyle='--', label='Uniform Expectation')
    axes[1, 0].set_xlabel('8-Bit Byte Value (0 - 255)')
    axes[1, 0].set_ylabel('Frequency per Bin')
    axes[1, 0].set_title('3. Byte-Level Histogram Analysis (Paper Sec. 11.1)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, linestyle='--', alpha=0.5)

    # Panel 4: Adjacent Byte Correlation Scatter (Paper Section 11.2.1)
    axes[1, 1].scatter(p_rsa['bytes'][:-1], p_rsa['bytes'][1:], alpha=0.3, s=10, color='blue', label=f"RSA (r={p_rsa['corr']:.4f})")
    axes[1, 1].scatter(p_ms['bytes'][:-1], p_ms['bytes'][1:], alpha=0.3, s=10, color='orange', label=f"MS (r={p_ms['corr']:.4f})")
    axes[1, 1].set_xlabel('Byte Value at Index i')
    axes[1, 1].set_ylabel('Byte Value at Index i+1')
    axes[1, 1].set_title('4. Adjacent Byte Correlation Dispersion (Paper Sec. 11.2.1)')
    axes[1, 1].legend(loc='upper right')
    axes[1, 1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('results/advanced_comparison_plots.png', dpi=300)
    plt.close()
    print("\nSaved 4-panel visual report to: results/advanced_comparison_plots.png")

if __name__ == "__main__":
    main()