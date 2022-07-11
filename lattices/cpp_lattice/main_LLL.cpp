#include "lattice_attacks.hpp"
#include <iostream>
#include <chrono>
 
int lift(int x, int mod){
    if(x > mod/2){
        return x - mod;
    }
    return x;
}
 
int main(){
    int dim;
    std::cin >> dim;
    Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic> base(dim, dim);
    for(int i = 0; i < dim; i++){
        for(int j = 0; j < dim; j++){
            std::cin >> base(i, j); 
        }
    }
    base.transposeInPlace();

    mpf_class c = base.col(0).norm();
    int k = 0;
    Eigen::VectorXd v = base.col(0);
    for(int i = 1; i < dim; i++){
        if(base.col(i).norm() < c){
            c = base.col(i).norm();
            k = i;
            v = base.col(i);
        }
    }

    std::cout << "Shortest vector:   " << v.transpose() << std::endl;
    std::cout << "It's length:       " << c << std::endl << std::endl;

    mpq_class delta, eta;
    //std::cin >> delta >> eta;
    delta = mpq_class(3, 4);
    eta = mpq_class(1, 2);
    std::cout << base << std::endl << std::endl;
    std::cout << "Hadamard Base: " << HadamardRatio(base) << std::endl;

    std::chrono::steady_clock::time_point begin, end;
    begin = std::chrono::steady_clock::now();
    LLL(base, delta, eta);
    end = std::chrono::steady_clock::now();
    
    std::cout << "Time Elapsed: " << std::chrono::duration_cast<std::chrono::microseconds>(end-begin).count()/1000000.0 << " s" << std::endl;

    std::cout << base << std::endl;
    std::cout << "Hadamard Reduced: " << HadamardRatio(base) << std::endl;
    if(!LLL_check(base, delta, eta)){
        std::cout << "FUCKING WHAT THE FUCK" << std::endl;
    }

    std::cout << "Gaussian Expected: " << GaussianExpectedShortestLength(base) << std::endl;
    std::cout << "Gaussian Appr:     " << GaussianExpectedAppr(base) << std::endl;

    c = base.col(0).norm();
    k = 0;
    v = base.col(0);
    for(int i = 1; i < dim; i++){
        if(base.col(i).norm() < c){
            c = base.col(i).norm();
            k = i;
            v = base.col(i);
        }
    }

    std::cout << "Shortest vector:   " << v.transpose() << std::endl;
    std::cout << "It's number:       " << k + 1 << std::endl;
    std::cout << "It's length:       " << c << std::endl << std::endl;

    std::cout << "Correct reduction?: " << LLL_check(base, delta, eta) << std::endl;
    return 0;
}
