#include <gmpxx.h>
#include <gmp.h>
#include <iostream>
#include <vector>

int main(int argc, char** argv){
	mpz_class n, d, e, g;
    n = "0x00ef32da3ccefd6a8ee6c48200a6ffeed52d30e6cda9f422edbcfb4319da31b997ac0912622049cd2c3582d372a14d0af974c7df689674a1f714c6c9027a93730d800e910eb197b8c2ea1ef7371cbeaf716758457df7adef3a192db0aff738bb7f119e08069ef258caa083b9de9db22936bca96262c60f506b68f2b4660b1667d55253dfa5d87b51df5deb93fb963b83f3aa2b0d3dd5dadf3ac87f930c809a5209d764fbfcc1beb24a4fca00b1b42f024220d38483eda8115e4b14c97a85fa15a2b03b042deac63046f66a2b3d5256e0ff58791dad2e3f7dc4360fb246782d9935dd420d1f2a4f75b4fbe1c6514dd9aced123a5deea63e3ac5fce9ceaf80006f919ed31c7c6c5e1c1bbc177c08a23a96efa70125f8338bf042f2d9d3cee05d554c8c9b5fca9157db719793e059b95ed9f57f38421095436ce6d696b990087a2d1601176a0b772d307201443556f031401798f9457458f6fc086b6705fe23573645ce8adb9a11bee56b6ca77ad6eb075813de3dfce178f0f087f66f7e948c7ca6ad";
    d = "0x69bd362249725727a2b5ddae4224c344737cb99ad2f57c7751e254f059b73f8edfdb06c85ff3a0025a096245bb2e5e9a95d841576fa35171f33a48e392a219eb2edfc19a1841b4c85d4ca10638ebc68cc01d9262b419acb627293e811b2d761d1f019814ad30feb55c2dbefdbd02641bb15cc3845c7faa9240cb8199d66eea29b00229cc9b9d303d28bc9a274e6b32d2853810db73ed145f5d00a05597882099ff20c21022e994d12ae2665a2807dbdcb5bc2b4952c6c81ec1dc0790e526ff6697ee2fdad983d0270cf04845373f14088d1b7f9d667dbac05d8621453b08f3ddb0f2541ef9296bcb2c4abb763c925c68fc6eff945ac3d8c16d8f5eb76b286da83b36ca72210dd93692d0ca70f4473a983c9a6d6abc3945bf971e93cd6fa40f1a20a9815ab37ed40e4660818e68baddbec1d19c5bd723635066b9c3ffc09234a477e6895f7048c1df2b39fe1016a27d097351d5288ac9ef3a4883d0d2010b41ca0758de174fcfd093bedbd01c16116a5e978fc624c28e7cfa266c0e78d9f3";
    g = "0x21a82259e3d5bc1140b1336a02ed9a2c4e75410ac8bc185fbb511daec66b75ca87c170b1325ffaebaf2c380a8cad89f006e804db7a386e270ca390029c2c1f8f41a438d6288fd74c984c7b4c859db43e1efd89524a3ad2045da93652ed56046fcf4df89487f05b5c530b50f5244efe4d67d79be86d92a37d0deb1bf0778eb9d2ac1f1bc635b6ffb2cec8d296be2d13f2daab2239785a7c2c7bb8f365c1ac7971af5a9e193ae0e73a68c31d65ca245c0e7a9e9f7c1b95a925209912255354c6ebfcddffc1e1c77e37b163177bac40315dc30b5f0141cc161d7735445c962087d0a9b21de94baaad8393d64f5dc551927b365afbdf3e4b939e6c5871f3c1ff3fecb0af5d3517570705666b50038feab514518bf2c49065e5a691f004f284bf86ce35f6c62b55e4a56773dd4b92664b95f52c63c8d7090c63e0591feccbab73bbf9b71c00b1c5ba2bfac97720d18148d03f83074eefadabf6692403ace51a303f1734188e432df7e981049f2b4f17dacd5f8ad787711cd72c87b1ce55b544aff17f";
	e = "0x10001";

    mpz_class t, k0, g0, gc, effg, extrapow;
    std::vector<mpz_class> prec;
    t = d * 256 * 256 + 1;
    k0 = e * t - 1;

    while (k0 % 2 == 0){
        k0 = k0 / 2;
//        std::cout << k0 << std::endl;
        mpz_powm(g0.get_mpz_t(), g.get_mpz_t(), k0.get_mpz_t(), n.get_mpz_t());
        mpz_gcd(gc.get_mpz_t(), g0.get_mpz_t(), n.get_mpz_t());
 //       std::cout << g0 << std::endl;
       if (gc != 1 && gc != n){
            std::cout << gc << std::endl;
            std::cout << "done" << std::endl;
            exit(0);
        }
        prec.push_back(g0);
    }
    mpz_powm(effg.get_mpz_t(), g.get_mpz_t(), e.get_mpz_t(), n.get_mpz_t());
        
    for (int i = 2; i < 256 * 256; i += 2){
        extrapow = i;
        int c = 0;

        while (extrapow % 2 == 0 && c < prec.size()){
            extrapow /= 2;

            mpz_powm(g0.get_mpz_t(), effg.get_mpz_t(), extrapow.get_mpz_t(), n.get_mpz_t());
            t = (prec[c] * g0) % n;
            t -= 1;
            t %= n;
            
            mpz_gcd(gc.get_mpz_t(), t.get_mpz_t(), n.get_mpz_t());


//            if (i == 58260){
//                std::cout << "pow " << extrapow << std::endl;
//                std::cout << "prec[c] " << prec[c] << std::endl;
//                std::cout << "effg ^ extrapow " << g0 << std::endl;
//                std::cout << "gcd " << gc << std::endl;
//                std::cout << "n " << n << std::endl;
//                std::cout << "G " << g << std::endl;
//                std::cout << "t " << t << std::endl;
//                std::cout << std::endl;
//            }

            if (gc != 1 && gc != n){
               std::cout << gc << std::endl;
               exit(0);
            }
            c++;
        }
    }
    return 0;
}
