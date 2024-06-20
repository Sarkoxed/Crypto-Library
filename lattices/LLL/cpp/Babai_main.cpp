#include "lattice_attacks.hpp"

int main(){
    int dim;
    std::cin >> dim;
    Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic> m(dim, dim);
    for(int i = 0; i < dim; i++){
        for(int j = 0; j < dim; j++){
            std::cin >> m(i, j);
        }
    }
    m.transposeInPlace();
    std::cout << m << std::endl;
    Eigen::Vector<mpz_class, Eigen::Dynamic>  t(dim);
    for(int i = 0; i < dim; i++){
        std::cin >> t(i);
    }
    std::cout << t << std::endl;

    Eigen::Vector<mpz_class, Eigen::Dynamic> a, b;
//    Babai_Closest_vertex(a, t, m);
    Babai_Closest_plain(b, t, m);

    std::cout << "Hadamard Ratio: " << HadamardRatio(m) << std::endl;
//    std::cout << a.transpose() << std::endl;
//    std::cout << (a - t).norm() << std::endl;
    std::cout << b.transpose() << std::endl;
    std::cout << (b - t).cast<mpf_class>().norm() << std::endl;

    Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic> oldbasis = m;
    LLL(m);
    if(m.cols() <= 10){
        std::cout << "Reduced: " << std::endl << m << std::endl;
    }
//    Babai_Closest_vertex(a, t, m);
    Babai_Closest_plain(b, t, m);

    std::cout << "Hadamard Ratio: " << HadamardRatio(m) << std::endl;
//    std::cout << a.transpose() << std::endl;
//    std::cout << (a - t).norm() << std::endl;
    std::cout << b.transpose() << std::endl;
    std::cout << (b - t).cast<mpf_class>().norm() << std::endl;
    
    Eigen::MatrixXd fbase(dim, dim);
    Eigen::VectorXd ftarget(dim);
    for(int  i = 0; i < dim; i++){
        for(int j = 0; j < dim; j++){
            fbase(i, j) = mpf_class(oldbasis(i, j)).get_d();
        }
        ftarget(i) = mpf_class(b(i)).get_d();
    }
    std::cout << fbase.colPivHouseholderQr().solve(ftarget) << std::endl;
    return 0;
}

