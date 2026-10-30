#include <iostream>
#include <boost/multiprecision/cpp_int.hpp>

using namespace boost::multiprecision;
using namespace std;

int main() {
    cpp_int massive_number = 1;
    
    // Calculate 100! (100 factorial)
    for(int i = 1; i <= 100; i++) {
        massive_number *= i; 
    }
    
    cout << "Boost is working! 100! is: \n" << massive_number << endl;
    return 0;
}