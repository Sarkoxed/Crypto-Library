#include <cstdint>
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

uint64_t mod = 1000000007;

std::vector<uint64_t> pows = {1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1,
                              0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1};

uint64_t inverse(uint64_t n) {
  uint64_t res = n;
  for (const auto i : pows) {
    res = (res * res) % mod;
    if (i == 1) {
      res = (res * n) % mod;
    }
  }
  return res;
}

uint64_t binomial(uint64_t n, uint64_t k) {
  if (k == 0) {
    return 1;
  }
  uint64_t num = 1;
  uint64_t den = 1;
  for (uint64_t i = 0; i <= k - 1; i++) {
    num = (num * (n - i)) % mod;
    den = (den * (i + 1)) % mod;
  }
  return num * inverse(den) % mod;
}

uint64_t get_n(uint64_t n) {
  std::vector<uint64_t> ass = {1, 1};
  uint64_t two_inv = inverse(2);
  for (uint64_t i = 2; i < n + 1; i++) {
    uint64_t tmp_s = 0;
    for (uint64_t j = 0; j < i; j++) {
      tmp_s += (binomial(i - 1, j) * ass[j] * ass[i - 1 - j]) % mod;
      tmp_s %= mod;
    }
    tmp_s = (tmp_s * two_inv) % mod;
    ass.push_back(tmp_s);
  }
  return ass.back();
}

uint64_t get_n1(uint64_t n) {
  std::unordered_map<int, uint64_t> A;
  A[-1] = 0;
  A[0] = 1;
  int k = 0;
  int e = 1;
  uint64_t Am = 0;
  for (uint64_t i = 0; i < n + 1; i++) {
    Am = 0;
    A[k + e] = 0;
    e = -e;
    for (uint64_t j = 0; j < i; j++) {
      Am = (Am + A[k]) % mod;
      A[k] = Am;
      k += e;
    }
  }
  return Am;
}

int main() {
  //    std::cout << get_n(25) << std::endl;
  for (uint64_t n = 2; n < 40; n++) {
    std::cout << get_n1(n + 1) << std::endl;
  }
  return 0;
}
