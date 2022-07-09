#include "LLL.hpp"
#include <iostream>
#include "../lattice_attacks.hpp"

bool LLL_check(Eigen::MatrixXd& base, double delta, double eta){
    Eigen::MatrixXd orthogonal(base.cols(), base.cols());
    Eigen::MatrixXd mu = Eigen::MatrixXd::Zero(base.cols(), base.cols());
    for(int i = 0; i < base.cols(); i++){
        orthogonal.col(i) = base.col(i);
        for(int j = 0; j < i; j++){
            double m = base.col(i).dot(orthogonal.col(j)) / orthogonal.col(j).squaredNorm();
            mu(i, j) = m;
            orthogonal.col(i) -= m * orthogonal.col(j);
        }
    }

    for(int i = 0; i < mu.cols(); i++){
        for(int j = 0; j < i; j++){
            if(fabs(mu(i, j)) > 1/2.0){
                return false;
            }
        }
    }
    for(int i = 1; i < base.cols(); i++){
        if(orthogonal.col(i).squaredNorm() < (delta - mu(i, i-1)*mu(i, i-1)) * orthogonal.col(i-1).squaredNorm()){
            return false;
        }
    }
    return true;
}


void LLL(Eigen::MatrixXd& base, double delta, double eta){
    int k = 1, kmax = 0, dim = base.cols();
    
    Eigen::MatrixXd orthogonal = Eigen::MatrixXd::Zero(dim, dim);
    orthogonal.col(0) = base.col(0);
    
    Eigen::MatrixXd mu = Eigen::MatrixXd::Zero(dim, dim);
    Eigen::VectorXd bs = Eigen::VectorXd::Zero(dim);
    bs(0) = base.col(0).squaredNorm();

    while(true){
        if(k > kmax){
            kmax = k;
            orthogonal.col(k) = base.col(k);

            for(int j = 0; j < k; j++){
                mu(k, j) = base.col(k).dot(orthogonal.col(j)) / bs(j);
                orthogonal.col(k) -= mu(k, j) * orthogonal.col(j);
            }
//           std::cout << orthogonal << std::endl << std::endl;
            bs(k) = orthogonal.col(k).squaredNorm();
        }

        while(true){
            reduce(k, k-1, eta, mu, base);
//            std::cout << "reduce\n" << base << std::endl << std::endl;
            if(bs(k) < (delta - mu(k, k-1)*mu(k, k-1)) * bs(k-1)){
                swap(k, kmax, mu, bs, base, orthogonal);
 //               std::cout << "swap" << std::endl;
 //               std::cout << base << std::endl << std::endl;
 //               std::cout << orthogonal << std::endl << std::endl;
                k = std::max(1, k-1);
                continue;
            }
            else{
                for(int l = k-2; l >= 0; l--){
                    reduce(k, l, eta, mu, base);
                }
                k++;
 //               std::cout << HadamardRatio(base) << std::endl;
            }

            if(k < dim){
                break;
            }
            else{
                return;
            }
        }
    }
}

void reduce(int k, int l, double eta, Eigen::MatrixXd& mu, Eigen::MatrixXd& base){
    if(fabs(mu(k, l)) <= eta){
        return;
    }

    double m = std::round(mu(k, l));
    base.col(k) -= m * base.col(l);
    mu(k, l) -= m;

    for(int i = 0; i <= l-1; i++){
        mu(k, i) -= m * mu(l, i);
    }
    return;
}

void swap(int k, int kmax, Eigen::MatrixXd& mu, Eigen::VectorXd& bs, Eigen::MatrixXd& base, Eigen::MatrixXd& orthogonal){
    Eigen::VectorXd tmp(base.cols());
    tmp = base.col(k);
    base.col(k) = base.col(k-1);
    base.col(k-1) = tmp;

    for(int j = 0; j <= k - 2; j++){
        std::swap(mu(k, j), mu(k-1, j));
    }

    double muu = mu(k, k-1);
    double B = bs(k) + muu * muu * bs(k-1);
    mu(k, k-1) = muu * bs(k-1) / B;

    Eigen::VectorXd a, b; 
    a = orthogonal.col(k) + muu * orthogonal.col(k-1);
    b = orthogonal.col(k-1) - mu(k, k-1) * a;
    orthogonal.col(k-1) = a;
    orthogonal.col(k) = b;

    bs(k) = bs(k-1) * bs(k) / B;
    bs(k-1) = B;
    for(int i = k+1; i <= kmax; i++){
        double m = mu(i, k);
        mu(i, k) = mu(i, k-1) - muu * m;
        mu(i, k-1) = m + mu(k, k-1) * mu(i, k);
    }
    return;
}



