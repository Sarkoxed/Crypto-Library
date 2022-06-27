#include <iostream>
#include "lattice_attacks.hpp"
#include "cmath"
// 137
// 312
// 215
// -187
// 53178
// 81743
int main(){
    int dim;
    std::cout << "Insert dimension: ";
    std::cin >> dim;

    Eigen::VectorXf w(dim), v(dim);
    Eigen::MatrixXf vecm(dim, dim);
    w << 1, 2;

    for(int i = 0; i < dim; i++){
        std::cout << "Your " << i + 1 << " vector: " << std::endl;
        for(int j = 0; j < dim; j++){
            std::cin >> vecm(j, i);
        }
    }
    std::cout << vecm;
    std::cout << std::endl << "Your vector: " << std::endl;
    for(int i = 0; i < dim; i++){
        std::cin >> w(i);
        
    }
    std::cout << w << std::endl;
    Babai_algorithm(v, w, vecm);
    std::cout << std::endl << "Your answer" << std::endl << v.transpose();


    std::cout << "distance: " << (v - w).norm() << std::endl;
    std::cout << "Hadamard Ratio: " << powf(fabs(vecm.determinant()) / vecm.col(0).norm() / vecm.col(1).norm(), 1.0/static_cast<float>(dim)) << std::endl;

    return 0;
}

