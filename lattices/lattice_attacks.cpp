#include <iostream>
#include <Eigen/Dense>
#include <math.h>

void Babai_algorithm(Eigen::VectorXf& v, Eigen::VectorXf& w, Eigen::MatrixXf& basis){
    Eigen::VectorXf ans = basis.colPivHouseholderQr().solve(w).array().rint().matrix();
    std::cout << ans;
    v = basis * ans;
}

void Gauss_Lattice_Reduction(Eigen::VectorXd& v1, Eigen::VectorXd& v2){
    int m;
    while(true){
        if(v1.norm() > v2.norm()){
            std::swap(v1, v2);
        }
        auto x = v1.dot(v2);
        auto r1 = v1.norm();
        auto r2 = v2.norm();
        m = round(v1.dot(v2) / (v1.norm() * v1.norm()));
        if(m == 0){
            return;
        }
        v2 -= m * v1;
    }
}

       
