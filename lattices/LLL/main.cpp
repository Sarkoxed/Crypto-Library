#include "LLL.hpp"
#include <iostream>
#include "../lattice_attacks.hpp"
int main(){
    int dim = 6;
    //std::cin >> dim;
    Eigen::MatrixXd base(dim, dim);
    base << 20, 51, 35, 59, 73, 73, 14, 48, 33, 61, 47, 83, 95, 41, 48, 84, 30, 45, 0, 42, 74, 79, 20, 21, 6, 41, 49, 11, 70, 67, 23, 36, 6, 1, 46, 4;
    //base << 2, 2, -4, 0, -2, 0, 17, 1, -1, 5, 0, 43, 1, -1, 1, 1, -1, -2, 1, 5, 1, -3, 3, -1, -1;
    //for(int i = 0; i < dim; i++){
    //    for(int j = 0; j < dim; j++){
    //        std::cin >> base(i, j);
    //    }
    //}

    double delta, eta;
    //std::cin >> delta >> eta;
    delta = 0.99;
    eta = 0.5;
    base.transposeInPlace();
    std::cout << base << std::endl << std::endl;
    LLL(base, delta, eta);
    std::cout << base << std::endl;
    std::cout << HadamardRatio(base) << std::endl;
    std::cout << LLL_check(base, delta, eta) << std::endl;
    if(!LLL_check(base, delta, eta)){
        std::cout << "FUCKING WHAT THE FUCK" << std::endl;
    }
    std::cout << "Shortest vector:   " << base.col(0).norm() << std::endl;
    std::cout << "Gaussian Expected: " << GaussianExpectedShortestLength(base) << std::endl;
    std::cout << "Gaussian Appr:     " << GaussianExpectedAppr(base) << std::endl;
    return 0;
}
