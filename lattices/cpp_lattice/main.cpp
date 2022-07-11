#include "lattice_attacks.hpp"

int main(){
    mpq_class a(101, 200), b(99, 200), c(100, 200), d(-101, 200);
    std::cout << nearest(a) << " " << a << std::endl;
    std::cout << nearest(b) << " " << b << std::endl;
    std::cout << nearest(c) << " " << c << std::endl;
    std::cout << mpf_class(d).get_si() << std::endl;
    std::cout << nearest(d) << " " << d << std::endl;
}
