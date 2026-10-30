#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>

using namespace std;

int main() {
    int length = 10000;
    uint16_t state = 0xACE1; 

    ofstream outfile("../results/nlfsr_output.txt");
    if (!outfile.is_open()) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    outfile << length << "\n";

    for (int i = 0; i < length; i++) {
        // Calculate the linear taps
        uint16_t linear_bit = ((state >> 0) ^ (state >> 2) ^ (state >> 3) ^ (state >> 5)) & 1;
        
        // Add non-linearity (AND gate on bits 1 and 4)
        uint16_t nonlinear_bit = ((state >> 1) & (state >> 4)) & 1;
        
        uint16_t bit = linear_bit ^ nonlinear_bit; // Combine them
        
        outfile << (state & 1) << " ";
        
        state = (state >> 1) | (bit << 15);
    }

    outfile.close();
    cout << "NLFSR generated. Saved to results/nlfsr_output.txt" << endl;
    return 0;
}