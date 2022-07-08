#include <iostream>
#include "lattice_attacks.hpp"

int main(){
    int dim;
    std::cout << "Insert dimension: ";
    std::cin >> dim;

    Eigen::VectorXf w(dim), v(dim);
//    Eigen::MatrixXf vecm(dim, dim);
//
//    for(int i = 0; i < dim; i++){
//        std::cout << "Your " << i + 1 << " vector: " << std::endl;
//        for(int j = 0; j < dim; j++){
//            std::cin >> vecm(j, i);
//        }
//    }
//    std::cout << vecm;
//    std::cout << std::endl << "Your vector: " << std::endl;
//    for(int i = 0; i < dim; i++){
//        std::cin >> w(i);
//        
//    }
//    std::cout << w << std::endl;
//    Babai_algorithm(v, w, vecm);
//    std::cout << std::endl << "Your answer" << std::endl << v.transpose();
//    
//    std::cout << std::endl << vecm << std::endl;
//    std::cout << std::endl << "distance: " << (v - w).norm() << std::endl;
//    std::cout << "Hadamard Ratio: "    << HadamardRatio(vecm)<< std::endl;
    Eigen::VectorXd v1(dim), v2(dim);
    v1 << 725734520, 613807887;
    v2 << 3433061338, 2903596381;
//    std::cout << std::endl << "Your vector: " << std::endl;
//    for(int i = 0; i < dim; i++){
//        std::cin >> v1(i);
//    }
//    std::cout << std::endl << "Your vector: " << std::endl;
//    for(int i = 0; i < dim; i++){
//        std::cin >> v2(i);
//    }
    std::cout << "Basis: " << v1.transpose() << std::endl << v2.transpose() << std::endl;
    Gauss_Lattice_Reduction(v1, v2);
    std::cout << "Reduced Basis: " << v1.transpose() << std::endl << v2.transpose() << std::endl;
    return 0;
}

