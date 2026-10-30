# Comparative Cryptographic Evaluation of RSA and Micali-Schnorr PRBGs

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![C++17](https://img.shields.io/badge/C++-17-blue.svg)
![Status: Completed](https://img.shields.io/badge/Status-Completed-success.svg)

## 📌 Project Overview
This repository contains the source code, experimental data, and analytical scripts for a comprehensive B.Tech project evaluating the cryptographic security, statistical randomness, and computational efficiency of the **Micali-Schnorr Pseudorandom Bit Generator (PRBG)** against the classical **Standard 1-Bit RSA Generator**. 

While classical RSA securely extracts only 1 bit per modular exponentiation cycle, the Micali-Schnorr optimization harvests a massive block of bits ($k = 251$ bits for a 256-bit modulus) per cycle. This project conducts a rigorous 4-phase empirical investigation to mathematically prove that this aggressive multi-bit extraction achieves a **251-fold reduction in computational overhead** without sacrificing algebraic security, statistical randomness, or introducing run-length compressibility.

---

## ⚙️ Cryptographic Environment & Constants
To ensure an exact, controlled comparison, both generators were implemented in C++ (using the Boost Multiprecision library) and locked to identical initial states:
*   **Modulus ($N$):** 256-bit composite integer.
*   **Public Exponent ($e$):** `65537` (Fermat prime).
*   **Extraction Rate ($k$):** 
    *   RSA: $k = 1$ bit / cycle
    *   Micali-Schnorr: $k = 251$ bits / cycle (derived via $k = \lfloor \log_2(N)(1 - 2/e) \rfloor - 1$).
*   **Sequence Length:** 10,000 bits generated per test condition.

---

## 🧪 Experimental Phases & Methodology

### Phase 1: Hardware LFSR Baseline vs. Prime Modulus Taxonomies
Benchmarked a hardware-oriented 16-bit Linear Feedback Shift Register (LFSR) against number-theoretic generators constructed using **Standard**, **Safe**, and **Sophie Germain** prime factorizations.
*   **LFSR Failure:** Demonstrated trivial vulnerability to the Berlekamp-Massey algorithm, with complexity permanently flatlining at $L = 16$ after just 32 bits.
*   **Number-Theoretic Resistance:** Both RSA and Micali-Schnorr achieved optimal theoretical linear complexity ($L \approx N/2 = 5000$) regardless of the prime taxonomy used, proving robust resistance to linear cryptanalysis.

### Phase 2: Multiplicative Subgroup Order Dependency
Isolated the impact of initial seed subgroup orders on linear complexity using a 256-bit Safe Prime modulus:
*   **Maximal Order (Seeds A & B):** Quadratic residues ($x_0 = 4, 9$) generated sequences that perfectly tracked the optimal complexity bound $L \approx N/2$.
*   **Degenerate Order (Seed C):** A trivial non-residue ($x_0 = N-1$) forced a state cycle of order 2. 
    *   *RSA* instantly collapsed at $L = 1$.
    *   *Micali-Schnorr* exhibited a unique **block-entropy cap**, plateauing at exactly $L = 251$ (the extraction block size) before structural failure.

### Phase 3: Foundational Beker-Piper Statistical Battery
Analyzed maximal-order 10,000-bit sequences across the 5 standard Beker-Piper randomness postulates:
1.  **Monobit Frequency Test:** Verified ideal 50/50 balance (Deviations $< 0.67\%$).
2.  **Serial Test:** Confirmed uniform transition distributions (00, 01, 10, 11).
3.  **Poker Test:** Evaluated 4-bit non-overlapping block distributions ($\chi^2 \approx 20.28$, well below the 24.996 threshold).
4.  **Runs Test:** Validated Golomb’s exponential decay postulate for contiguous sequences of 0s and 1s.
5.  **Lag-1 Autocorrelation:** Confirmed zero periodic repeating dependencies.

### Phase 4: Advanced Information-Theoretic & Compression Analysis
Conducted rigorous byte-level and compression analysis by mapping 10,000-bit streams into 1,250 contiguous 8-bit bytes ($0-255$):
*   **Maurer's Universal Statistical Test:** Proved zero multi-bit periodic memory across block sizes $L \in \{4, 5, 6\}$.
*   **Tuple-Wise Huffman Coding:** Encoded alternating `(bit, run_length)` tuples. Demonstrated exact adherence to ideal dyadic decay ($2^{-(r+1)}$), yielding a Tuple Entropy of $\approx 3.00$ bits/run and a pure RLE compression ratio of $0.9999$ (Complete Incompressibility).
*   **Byte-Level GLCM & Entropy Metrics (Adapted from Baowidan et al.):**
    *   **Shannon Entropy:** Reached the Miller-Madow finite-sample theoretical maximum ($7.8459$ and $7.8613$ bits).
    *   **Adjacent Byte Correlation:** Near-zero dispersion ($r \approx 0$) across the $256 \times 256$ phase space.
    *   **GLCM Metrics:** Minimal Homogeneity, negligible Energy, and massive Contrast, indicating completely unpredictable byte transitions.
*   **Cross-Stream Divergence:** Sequences initialized from the exact same seed diverged immediately (NPCR = $99.60\%$, UACI = $33.08\%$, PSNR = $7.84$ dB), proving multi-bit extraction generates an entirely independent and orthogonal keystream.

---

## 🏆 Key Conclusions
1.  **Exact Cryptographic Parity:** Extracting $251$ bits per iteration introduces **zero degradation** in algebraic complexity, statistical randomness, information density, or run-length incompressibility compared to extracting 1 bit.
2.  **Decisive Architectural Superiority:** The Micali-Schnorr PRBG achieves a **$251\times$ computational throughput speedup** over classical RSA, rendering it the conclusively superior architecture for practical symmetric stream cipher applications.

---

## 📁 Repository Structure
*   `/src`: C++ source files for the LFSR, RSA, and Micali-Schnorr sequence generators (Boost Multiprecision).
*   `/scripts`: Python scripts for executing the Berlekamp-Massey algorithm, Beker-Piper battery, and advanced Phase 4 metrics (`statistical_test.py`, `advanced_comparison_test.py`).
*   `/data`: Generated 10,000-bit output sequences for various seeds and prime moduli.
*   `/results`: Visualizations, complexity profiles, and terminal output logs.
*   `/report`: LaTeX source code and the final compiled IEEE Conference B.Tech Project Report.

## 🚀 How to Run the Tests
1. Generate the bit sequences using the C++ generators (requires `g++` and `libboost-all-dev`).
2. Run the statistical analysis suites:
   ```bash
   python scripts/statistical_test.py
   python scripts/advanced_comparison_test.py
   ```