#include "LLL.hpp"
#include <iostream>
#include "../lattice_attacks.hpp"
int main(){
    int dim = 5;
    Eigen::MatrixXd base(dim, dim);
    base << 2, 2, -4, 0, -2, 0, 17, 1, -1, 5, 0, 43, 1, -1, 1, 1, -1, -2, 1, 5, 1, -3, 3, -1, -1;
    base.transposeInPlace();
    std::cout << base << std::endl << std::endl;
    LLL(base);
    std::cout << base << std::endl;
    std::cout << HadamardRatio(base) << std::endl;
    return 0;
}
