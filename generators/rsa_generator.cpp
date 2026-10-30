#include <iostream>
#include <fstream>
#include <boost/multiprecision/cpp_int.hpp>

using namespace boost::multiprecision;
using namespace std;

int main() {
    int length = 10000;
    
    // // Two standard 128-bit prime numbers (written in hexadecimal)
    // cpp_int p("0x2EAEB02951AB44A0D23FDBB90844F353"); 
    // cpp_int q("0x303EBC6D0F9DFAD17E6FF17B4AA76DD7");


    //safe primes
    cpp_int p("0xD4709E839EB00C12BEB23FB4AC3E7C97"); 
    cpp_int q("0xFA3C68CD1D7B481B09886E24FD50B77B");
    
    //sophie german
    // cpp_int p("0x6A384F41CF5806095F591FDA561F3E4B"); 
    // cpp_int q("0x7D1E34668EBD240D84C437127EA85BBD");

    cpp_int N = p * q;
    cpp_int e = 65537;
    
    // cpp_int seed = 123456789; // Initial state x_0(used for the 1st experiment)

    //experiment - 2 (order vs complexity for safe primes)
    // cpp_int seed = 4;//order = p*q(quadratic residue)
    // cpp_int seed = 9;//order = p*q(quadratic residue)
    cpp_int seed = N-1;//order = 2
    cpp_int x = seed;

    //../results/rsa_standard_output.txt
    //../results/rsa_safe_output.txt
    //../results/rsa_sophie_output.txt
    ofstream outfile("../results/rsa_seed_c.txt");
    if (!outfile.is_open()) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    outfile << length << "\n";

    for(int i = 0; i < length; i++) {
        // x = (x^e) mod N
        x = powm(x, e, N);
        
        // Extract the Least Significant Bit
        int bit = static_cast<int>(x & 1);
        outfile << bit << " ";
    }

    outfile.close();
    cout << "RSA (Standard Primes) generated. Saved to results/rsa_standard_output.txt" << endl;
    return 0;
}