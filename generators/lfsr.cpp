#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>

using namespace std;

int main() {
    int length = 10000;
    uint16_t state = 0xACE1; // A non-zero starting seed

    ofstream outfile("../results/lfsr_output.txt");
    if (!outfile.is_open()) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    outfile << length << "\n"; // Output 'len' for the test scripts

    for (int i = 0; i < length; i++) {
        // Taps for 16-bit linear feedback
        uint16_t bit = ((state >> 0) ^ (state >> 2) ^ (state >> 3) ^ (state >> 5)) & 1;
        
        outfile << (state & 1) << " "; // Output the rightmost bit
        
        state = (state >> 1) | (bit << 15); // Shift and insert feedback
    }

    outfile.close();
    cout << "LFSR generated. Saved to results/lfsr_output.txt" << endl;
    return 0;
}