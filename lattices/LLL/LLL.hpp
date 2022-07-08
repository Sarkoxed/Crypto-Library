#include <Eigen/Dense>
#include <algorithm>

void LLL(Eigen::MatrixXd&, double delta=0.75, double eta=0.5);
void reduce(int, int, double, Eigen::MatrixXd&, Eigen::MatrixXd&);
void swap(int, int, Eigen::MatrixXd&, Eigen::VectorXd&, Eigen::MatrixXd&, Eigen::MatrixXd&);
