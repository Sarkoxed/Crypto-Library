#include "lattice_attacks.hpp"

int main(){
    int d = 2;
    Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic> m(2,2);
    m << 846835985, 9834798552, 87502093, 123094980;
    std::cout << m << std::endl;
    m.transposeInPlace();

    Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic> m1 = m;
    LLL(m);
    std::cout << m << std::endl;

    Eigen::Vector<mpz_class, Eigen::Dynamic> a, b;
    a = m1.col(0);
    b = m1.col(1);

    GaussLatticeReduction(a, b);
    std::cout << a << b << std::endl;
}
