import math

def read_sequence(filepath):
    try:
        with open(filepath, 'r') as f:
            # Replaces newlines AND spaces, leaving only a pure string of 0s and 1s
            return f.read().replace('\n', '').replace(' ', '').strip()
    except FileNotFoundError:
        return None

def frequency_test(seq):
    n = len(seq)
    n1 = seq.count('1')
    n0 = seq.count('0')
    ideal = n / 2
    dev_1 = abs(n1 - ideal) / ideal * 100
    return n0, n1, dev_1

def serial_test(seq):
    pairs = {'00': 0, '01': 0, '10': 0, '11': 0}
    for i in range(len(seq) - 1):
        pairs[seq[i:i+2]] += 1
    return pairs

def poker_test(seq, m=4):
    blocks = [seq[i:i+m] for i in range(0, len(seq) - len(seq)%m, m)]
    counts = {}
    for block in blocks:
        counts[block] = counts.get(block, 0) + 1
    
    # Calculate Chi-Square statistic
    k = 2**m
    n_blocks = len(blocks)
    chi_square = sum(((counts.get(format(i, f'0{m}b'), 0) - (n_blocks/k))**2) / (n_blocks/k) for i in range(k))
    return chi_square

def runs_test(seq):
    runs = {'1': {}, '0': {}}
    current_bit = seq[0]
    current_length = 1
    
    for i in range(1, len(seq)):
        if seq[i] == current_bit:
            current_length += 1
        else:
            runs[current_bit][current_length] = runs[current_bit].get(current_length, 0) + 1
            current_bit = seq[i]
            current_length = 1
    runs[current_bit][current_length] = runs[current_bit].get(current_length, 0) + 1
    
    # Return count of runs of length 1, 2, and 3+
    def summarize(bit):
        return (runs[bit].get(1, 0), runs[bit].get(2, 0), sum(v for k, v in runs[bit].items() if k >= 3))
    
    return summarize('0'), summarize('1')

def autocorrelation_test(seq, shift=1):
    n = len(seq)
    matches = sum(1 for i in range(n - shift) if seq[i] == seq[i + shift])
    mismatches = (n - shift) - matches
    return matches, mismatches

def run_all_tests():
    seq_rsa = read_sequence('results/rsa_seed_a.txt')
    seq_ms = read_sequence('results/ms_seed_a.txt')

    if not seq_rsa or not seq_ms:
        print("Error: Could not find sequence files in 'results/' directory.")
        return

    n = len(seq_rsa)
    print(f"{'TEST METRIC':<25} | {'RSA (1-bit)':<25} | {'MICALI-SCHNORR (251-bit)':<25}")
    print("-" * 80)
    
    # 1. Frequency
    r0, r1, r_dev = frequency_test(seq_rsa)
    m0, m1, m_dev = frequency_test(seq_ms)
    print(f"1. Frequency (0s / 1s)    | {r0} / {r1} ({r_dev:.2f}% dev)  | {m0} / {m1} ({m_dev:.2f}% dev)")
    
    # 2. Serial
    r_ser = serial_test(seq_rsa)
    m_ser = serial_test(seq_ms)
    print(f"2. Serial (00/01/10/11)   | {r_ser['00']}/{r_ser['01']}/{r_ser['10']}/{r_ser['11']} | {m_ser['00']}/{m_ser['01']}/{m_ser['10']}/{m_ser['11']}")
    
    # 3. Poker (m=4)
    r_poker = poker_test(seq_rsa)
    m_poker = poker_test(seq_ms)
    print(f"3. Poker (Chi-Square)     | {r_poker:.2f} (Ideal: ~15.0)     | {m_poker:.2f} (Ideal: ~15.0)")
    
    # 4. Runs
    r_r0, r_r1 = runs_test(seq_rsa)
    m_r0, m_r1 = runs_test(seq_ms)
    print(f"4. Runs of 0s (L: 1/2/3+) | {r_r0[0]}/{r_r0[1]}/{r_r0[2]}               | {m_r0[0]}/{m_r0[1]}/{m_r0[2]}")
    print(f"   Runs of 1s (L: 1/2/3+) | {r_r1[0]}/{r_r1[1]}/{r_r1[2]}               | {m_r1[0]}/{m_r1[1]}/{m_r1[2]}")
    
    # 5. Autocorrelation (Shift=1)
    r_ac = autocorrelation_test(seq_rsa, 1)
    m_ac = autocorrelation_test(seq_ms, 1)
    print(f"5. Autocorrelation (d=1)  | Match: {r_ac[0]}, Mis: {r_ac[1]} | Match: {m_ac[0]}, Mis: {m_ac[1]}")
    print("-" * 80)

if __name__ == "__main__":
    run_all_tests()