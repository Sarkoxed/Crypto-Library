#include <Eigen/Dense>
#include <cmath>
#include <limits>
#include <iostream>
#include <algorithm>
#include <gmpxx.h>
#include <mpreal.h>

#pragma once 
mpz_class nearest(mpq_class);

double HadamardRatio(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>&);
double GaussianExpectedShortestLength(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& base);
double GaussianExpectedAppr(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& base);

void GramSchmidt(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& basis, Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic>& orth);
void Babai_Closest_vertex(Eigen::Vector<mpz_class, Eigen::Dynamic>& v, Eigen::Vector<mpz_class, Eigen::Dynamic>& w, Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& basis);
void Babai_Closest_plain(Eigen::Vector<mpz_class, Eigen::Dynamic>& v, Eigen::Vector<mpz_class, Eigen::Dynamic>& w, Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>& basis);
void Gauss_Lattice_Reduction(Eigen::Vector<mpz_class, Eigen::Dynamic>&, Eigen::Vector<mpz_class, Eigen::Dynamic>&);

void LLL(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>&, mpq_class delta=mpq_class(3, 4), mpq_class eta=mpq_class(1,2));
void reduce(int, int, mpq_class, Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic>&, Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>&);
void swap(int, int, Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic>&, Eigen::Vector<mpq_class, Eigen::Dynamic>&, Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>&, Eigen::Matrix<mpq_class, Eigen::Dynamic, Eigen::Dynamic>&);
bool LLL_check(Eigen::Matrix<mpz_class, Eigen::Dynamic, Eigen::Dynamic>&, mpq_class delta=mpq_class(3, 4), mpq_class eta=mpq_class(3, 4));


