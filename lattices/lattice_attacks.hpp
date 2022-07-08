#include <Eigen/Dense>
#include <cmath>

void Babai_algorithm(Eigen::VectorXf&, Eigen::VectorXf&, Eigen::MatrixXf&);

void Gauss_Lattice_Reduction(Eigen::VectorXd&, Eigen::VectorXd&);

template <typename matr>
float HadamardRatio(matr& b){
    float de = b.determinant();
    int d = b.cols();
    float prod = 1.0;
    for(int i = 0; i < d; i++){
        prod *= b.col(i).norm();
    }
    return powf(fabs(de) / prod, 1.0 / static_cast<float>(d));
}


