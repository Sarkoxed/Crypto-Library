#include <gmpxx.h>
#include <iostream>
using namespace std;

int main(int argc, char** argv){
	int piska = atoi(argv[1]);
	mpz_class m, c, p, q, dbeg, e;
	m = "0x8ec212bec6d7dac8ec8804d8ce2fac0bc10c2fac2b248b673e0806a8b84d7470";
	c = "0xbeef";
	p = "0xffffffffffffffffffffffffffffff53";
	q = "0xffffffffffffffffffffffffffffff61";
	dbeg = "96074494030011676284860716315865778760";
	e = "0x10001";
	mpz_class m1 = m % p;
	mpz_class n = p*q;
	for (mpz_class i = piska; i < 0x10000000; i+=24){
		mpz_class x = dbeg + i * 4096;
		//x = "0x4847464544434241000055CB7546AA48";
		mpz_class r = (p-1) * (x-1);
		mpz_class r2 = -1;
		mpz_class d;
		mpz_powm(d.get_mpz_t(), e.get_mpz_t(), r2.get_mpz_t(), r.get_mpz_t());
		mpz_class res;
		mpz_powm(res.get_mpz_t(), c.get_mpz_t(), d.get_mpz_t(), n.get_mpz_t());
		if (res == m) cout << d << endl << x << endl;
	}
}

