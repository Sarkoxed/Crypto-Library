#include "lattice_attacks.hpp"

mpz_class nearest(mpq_class x){
    mpz_class a = mpf_class(x).get_si();
    mpq_class b = x - a;
    mpq_abs(b.get_mpq_t(), b.get_mpq_t());
    if(b <= mpq_class(1, 2)){
        return a;
    }
    else if(x < 0){
        return mpf_class(x - 1).get_si();
    }
    return mpf_class(x + 1).get_si();
}

double HadamardRatio(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& b){
    double det = b.cast<double>().determinant();
        
    int dim = b.cols();
    double prod = 1.0;
    for(int i = 0; i < dim; i++){
        prod *= b.col(i).cast<double>().norm();
    }
    det = fabs(det) / prod;
    return powf(det, 1.0/dim);
}

double GaussianExpectedShortestLength(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& base){
    double fac = tgamma(1 + base.cols() / 2.0);
    fac *= fabs(base.cast<double>().determinant());
    fac = pow(fac, 1.0/base.cols());
    fac *= sqrt(M_1_PI);
    return fac;
}

double GaussianExpectedAppr(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& base){
    double fac = pow(fabs(base.cast<double>().determinant()), 1.0/base.cols());
    fac *= sqrt(base.cols() / (2.0 * M_E) * M_1_PI);
    return fac;
}

void GramSchmidt(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& basis, Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic>& orth){
    orth.setZero();
    mpq_class m, dot;
    for(int i = 0; i < basis.cols(); i++){
        orth.col(i) = basis.col(i).cast<mpq_class>();
        for(int j = 0; j < i; j++){
            dot = basis.col(i).cast<mpq_class>().dot(orth.col(i));
            m = dot / orth.col(i).squaredNorm();
            orth.col(i) -= m * orth.col(j);
        }
    }
}

//void Babai_Closest_vertex(Eigen::Vector<mpz_class, Eigen::Dynamic>& v, Eigen::Vector<mpz_class, Eigen::Dynamic>& w, Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& basis){
//    Eigen::Vector<mpz_class, Eigen::Dynamic> ans = basis.colPivHouseholderQr().solve(w).array().rint().matrix();
//    v = basis * ans;
//}

void Babai_Closest_plain(Eigen::Vector<mpz_class, Eigen::Dynamic>& v, Eigen::Vector<mpz_class, Eigen::Dynamic>& t, Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& basis){
    Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic> orthogonal(basis.cols(), basis.cols());
    GramSchmidt(basis, orthogonal);
    Eigen::Vector<mpz_class, Eigen::Dynamic> ans = t;
    Eigen::Vector<mpq_class, Eigen::Dynamic> x, y;
    for(int i = basis.cols()-1; i >= 0; i--){
        y = orthogonal.col(i);
        ans = ans - nearest(x.cast<mpq_class>().dot(y) / y.squaredNorm()) * basis.col(i);
    }
    v = t - ans;
}


void GaussLatticeReduction(Eigen::Vector<mpz_class, Eigen::Dynamic>& v1, Eigen::Vector<mpz_class, Eigen::Dynamic>& v2){
    mpz_class m;
    while(true){
        if(v1.squaredNorm() > v2.squaredNorm()){
            std::swap(v1, v2);
        }
        m = nearest(v1.dot(v2) / (v1.norm() * v1.norm()));
        if(m == 0){
            return;
        }
        v2 -= m * v1;
    }
}



bool LLL_check(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& base, mpq_class delta, mpq_class eta){
    Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic> orthogonal(base.cols(), base.cols());
    Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic> mu = Eigen::MatrixXd::Zero(base.cols(), base.cols()).cast<mpq_class>();
    mpq_class m;
    for(int i = 0; i < base.cols(); i++){
        orthogonal.col(i) = base.col(i).cast<mpq_class>();
        for(int j = 0; j < i; j++){
            m = base.col(i).cast<mpq_class>().dot(orthogonal.col(j)) / orthogonal.col(j).squaredNorm();
            mu(i, j) = m;
            orthogonal.col(i) -= m * orthogonal.col(j);
        }
    }

    for(int i = 0; i < mu.cols(); i++){
        for(int j = 0; j < i; j++){
            if(abs(mu(i, j)) > eta){
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


void LLL(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& base, mpq_class delta, mpq_class eta){
    int k = 1, kmax = 0, dim = base.cols();
    
    Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic> orthogonal = Eigen::MatrixXi::Zero(dim, dim).cast<mpq_class>();
    orthogonal.col(0) = base.col(0).cast<mpq_class>();
    
    Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic> mu = Eigen::MatrixXi::Zero(dim, dim).cast<mpq_class>();
    Eigen::Vector<mpq_class, Eigen::Dynamic> bs = Eigen::VectorXi::Zero(dim).cast<mpq_class>();
    bs(0) = base.col(0).squaredNorm();

    while(true){
        if(k > kmax){
            kmax = k;
            orthogonal.col(k) = base.col(k).cast<mpq_class>();

            for(int j = 0; j < k; j++){
                mu(k, j) = base.col(k).cast<mpq_class>().dot(orthogonal.col(j)) / bs(j);
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

void reduce(int k, int l, mpq_class eta, Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic>& mu, Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& base){
    if(abs(mu(k, l)) <= eta){
        return;
    }

    mpz_class m = nearest(mu(k, l));
    base.col(k) -= m * base.col(l);
    mu(k, l) -= m;

    for(int i = 0; i <= l-1; i++){
        mu(k, i) -= m * mu(l, i);
    }
    return;
}

void swap(int k, int kmax, Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic>& mu, Eigen::Vector<mpq_class, Eigen::Dynamic>& bs, Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& base, Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic>& orthogonal){
    Eigen::Vector<mpz_class, Eigen::Dynamic> tmp(base.cols());
    tmp = base.col(k);
    base.col(k) = base.col(k-1);
    base.col(k-1) = tmp;

    for(int j = 0; j <= k - 2; j++){
        std::swap(mu(k, j), mu(k-1, j));
    }

    mpq_class muu = mu(k, k-1);
    mpq_class B = bs(k) + muu * muu * bs(k-1);
    mu(k, k-1) = muu * bs(k-1) / B;

    Eigen::Vector<mpq_class, Eigen::Dynamic> a, b; 
    a = orthogonal.col(k) + muu * orthogonal.col(k-1);
    b = orthogonal.col(k-1) - mu(k, k-1) * a;
    orthogonal.col(k-1) = a;
    orthogonal.col(k) = b;

    bs(k) = bs(k-1) * bs(k) / B;
    bs(k-1) = B;
    mpq_class m;
    for(int i = k+1; i <= kmax; i++){
        m = mu(i, k);
        mu(i, k) = mu(i, k-1) - muu * m;
        mu(i, k-1) = m + mu(k, k-1) * mu(i, k);
    }
    return;
}

     
