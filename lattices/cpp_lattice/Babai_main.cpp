#include <iostream>
#include <iomanip>
#include "lattice_attacks.hpp"

int main(){
    int dim;
    std::cin >> dim;
    Eigen::MatrixXd m(dim, dim);
    for(int i = 0; i < dim; i++){
        for(int j = 0; j < dim; j++){
            std::cin >> m(i, j);
        }
    }
    m.transposeInPlace();
    Eigen::VectorXd t(dim);
    for(int i = 0; i < dim; i++){
        std::cin >> t(i);
    }

    Eigen::VectorXd a, b;
    Babai_Closest_vertex(a, t, m);
    Babai_Closest_plain(b, t, m);

    std::cout << "Hadamard Ratio: " << HadamardRatio(m) << std::endl;
    std::cout << a.transpose() << std::endl;
    std::cout << (a - t).norm() << std::endl;
    std::cout << b.transpose() << std::endl;
    std::cout << (b - t).norm() << std::endl;

    Eigen::MatrixXd oldbasis = m;
    LLL(m);
    if(m.cols() <= 10){
        std::cout << "Reduced: " << std::endl << m << std::endl;
    }
    Babai_Closest_vertex(a, t, m);
    Babai_Closest_plain(b, t, m);

    std::cout << "Hadamard Ratio: " << HadamardRatio(m) << std::endl;
    std::cout << a.transpose() << std::endl;
    std::cout << (a - t).norm() << std::endl;
    std::cout << b.transpose() << std::endl;
    std::cout << std::setprecision(20) << (b - t).norm() << std::endl;

    std::cout << oldbasis.colPivHouseholderQr().solve(a) << std::endl;
    std::cout << oldbasis.colPivHouseholderQr().solve(b) << std::endl;



    return 0;
}

