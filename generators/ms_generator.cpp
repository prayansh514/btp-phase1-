#include <iostream>
#include <fstream>
#include <boost/multiprecision/cpp_int.hpp>

using namespace boost::multiprecision;
using namespace std;

// Function to count the total number of bits in a cpp_int
int get_bit_length(cpp_int n) {
    int bits = 0;
    while (n > 0) {
        bits++;
        n >>= 1;
    }
    return bits;
}

int main() {
    int target_length = 10000;
    
    // The same standard 128-bit prime numbers for a 1-to-1 comparison
    // cpp_int p("0x2EAEB02951AB44A0D23FDBB90844F353"); 
    // cpp_int q("0x303EBC6D0F9DFAD17E6FF17B4AA76DD7");

    //safe primes
    // cpp_int p("0xD4709E839EB00C12BEB23FB4AC3E7C97"); 
    // cpp_int q("0xFA3C68CD1D7B481B09886E24FD50B77B");

    //sophie german
    cpp_int p("0x6A384F41CF5806095F591FDA561F3E4B"); 
    cpp_int q("0x7D1E34668EBD240D84C437127EA85BBD");
    
    cpp_int N = p * q;
    cpp_int e = 65537;
    
    // Calculate k: the number of bits to extract per iteration
    // Formula: k = floor(log2(N) * (1 - 2/e))
    int bit_len_N = get_bit_length(N);
    int k = bit_len_N - (2 * bit_len_N) / 65537 - 1; // Simplified integer math for extraction
    
    //experiment - 2 (order vs complexity for safe primes)
    // cpp_int seed = 4;//order = p*q(quadratic residue)
    // cpp_int seed = 9;//order = p*q(quadratic residue)
    cpp_int seed = N-1;//order = 2
    cpp_int x = seed;

    //../results/ms_standard_output.txt
    //../results/ms_safe_output.txt
    //../results/ms_sophie_output.txt
    ofstream outfile("../results/ms_seed_c.txt");
    if (!outfile.is_open()) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    outfile << target_length << "\n";

    int bits_generated = 0;
    
    while(bits_generated < target_length) {
        x = powm(x, e, N);
        
        // Extract the top 'k' bits
        cpp_int temp = x;
        for (int i = 0; i < k && bits_generated < target_length; i++) {
            int bit = static_cast<int>(temp & 1);
            outfile << bit << " ";
            temp >>= 1; // Shift to get the next bit in the chunk
            bits_generated++;
        }
    }

    outfile.close();
    cout << "Micali-Schnorr generated. Extracted " << k << " bits per cycle. Saved to ms_standard_output.txt" << endl;
    return 0;
}