#include <iostream>
#include <sigpack.h>

using namespace arma;
using namespace sp;

int main() {
    vec b;
    b = fir1(7, 0.35);
    std::cout << "Filter coeffs: \\n" << b.t() << std::endl;
}
