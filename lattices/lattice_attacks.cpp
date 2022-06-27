#include <iostream>
#include <Eigen/Dense>

void Babai_algorithm(Eigen::VectorXf& v, Eigen::VectorXf& w, Eigen::MatrixXf& basis){
    Eigen::VectorXf ans = basis.colPivHouseholderQr().solve(w).array().round().matrix();
    std::cout << ans;
    v = basis * ans;
}
