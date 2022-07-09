#include "LLL.hpp"
#include <iostream>
#include "../lattice_attacks.hpp"
#include <chrono>
 
int power(int x, int y, int p){
    int res = 1;
    while (y > 0) {
        if (y % 2 == 1)
            res = (res * x) % p;
        y = y >> 1;
        x = (x * x) % p;
    }
    return res % p;
}
int lift(int x, int mod){
    if(x > mod/2){
        return x - mod;
    }
    return x;
}
 
int main(){
    int dim;
    std::cin >> dim;
    //int q;
    //std::cin >> q;
    Eigen::MatrixXi bas = Eigen::MatrixXi::Random(dim, dim);
    bas = bas.unaryExpr([](const int x) { return lift(x % 10000, 10000); });
    while(bas.cast<double>().determinant() == 0){
        bas.setRandom();
        bas = bas.unaryExpr([](const int x) { return lift(x % 10000, 10000); });
    }
    Eigen::MatrixXd base = bas.cast<double>();
    //for(int i = 0; i < dim; i++){
    //    for(int j = 0; j < dim; j++){
    //        base(i, j) = power(i+1 + dim, j+1, q); 
    //    }
    //}
    //base.transposeInPlace();

    double c = base.col(0).norm();
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


    double delta, eta;
    //std::cin >> delta >> eta;
    delta = 0.75;
    eta = 0.5;
//    std::cout << base << std::endl << std::endl;
    std::cout << "Hadamard Base: " << HadamardRatio(base) << std::endl;

    std::chrono::steady_clock::time_point begin, end;
    begin = std::chrono::steady_clock::now();
    LLL(base, delta, eta);
    end = std::chrono::steady_clock::now();
    
    std::cout << "Time Elapsed: " << std::chrono::duration_cast<std::chrono::microseconds>(end-begin).count()/1000000.0 << " mcs" << std::endl;

//    std::cout << base << std::endl;
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
