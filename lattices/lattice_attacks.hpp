#include <Eigen/Dense>
#include <cmath>
#include <math.h>

void Babai_algorithm(Eigen::VectorXf&, Eigen::VectorXf&, Eigen::MatrixXf&);

void Gauss_Lattice_Reduction(Eigen::VectorXd&, Eigen::VectorXd&);

template <typename matr>
double HadamardRatio(matr& b){
    double de = b.determinant();
    int d = b.cols();
    double prod = 1.0;
    for(int i = 0; i < d; i++){
        prod *= b.col(i).norm();
    }
    return powf(fabs(de) / prod, 1.0 / static_cast<float>(d));
}

template <typename matr>
double GaussianExpectedShortestLength(matr& base){
    double fac = tgamma(1 + base.cols() / 2.0);
    fac *= fabs(base.determinant());
    fac = pow(fac, 1.0/base.cols());
    fac *= sqrt(M_1_PI);
    return fac;
}

template <typename matr>
double GaussianExpectedAppr(matr& base){
    double fac = pow(fabs(base.determinant()), 1.0/base.cols());
    fac *= sqrt(base.cols() / (2.0 * M_E) * M_1_PI);
    return fac;
}
