#include <iostream>
#include <gmpxx.h>
#include <string>
#include <vector>
mpz_class m("0x206218e8c5e3b527a162ea56184e18012b6b982098bfe86d408d144f7296442186248f37016bc3eb256dfb1ff0a262f991b79cd7749299515f75a1115bff2bf0994d1f0b0d603c2a105a18e9a9910043ded1ed1eb1f242184d31322e001157cd7b3a9fa55519ee21d5973c94cde0d67bf574ebb14e50061626f6261");
mpz_class c("0x51af6f1638a957e2946e8a98afff5d1710ab43594b63fc01397720f88e89f54342b9f5eec8eb92b8fb4e381b5cda391b92ea242bea4baa7eb50a53d37bd385b5825a407fe95c5f787bb468f8d7fc0ec1b5d181e14bb790afd4d754ffc2c867c729b714351eb5db86961f7d416a297f02eb38f0ab838991f2e5c1f9f584");
mpz_class n("0x8da842199cf73a7ece7e236131c2b522846ec2b1c913a18f122ac30ed2324715447f140152ac3519399e53cd9b671ff2d9c4539ff3f9b4f05dd78e2b592ab86043546735f52a96db45874b3d377fe9ea2b4e05486eed2c47fd79047467b4245827fb1c98551d2de31a1a40826b8035ecb1f3b67cc82eb5783595b9c447");
mpz_class e("0x10001");
mpz_class p("0xe82ac35e9afe3210e3ba8a863ba9aa91504c97dcc4f53ea32d2228acbba95784ce004757ae7632da6d44f3dc1bb7fb4310c87c8fc8cbb9eedf602646b1265");
mpz_class q("0x9c32f124fdb987c8073cca6ee6d572b21ad03be79fbc9aaa1676e751573f38f5a5feb8fcf31af5cfb2efbea2d740d0ab8a68b859eb56cc55c8efe53fe7b3b");
//mpz_class a("0x206218e8c5e3b527a162ea56184e18012b6b982098bfe86d408d144f7296442186248f37016bc3eb256dfb1ff0a262f991b79cd7749299515f75a1115bff2bf0994d1f0b0d603c2a105a18e9a9910043ded1ed1eb1f242184d31322e001157cd7b3a9fa55519ee21d5973c94cde0d67bf574ebb14e50061626f6261"); 
mpz_class d("0xa39da43b51417d1eda02777adbaeb8e8956e19129fdd3ccdb37e10ae1dba54c00bcd7b9dcb8f7c0516b7f8b392bb19fbb5eb3d6b92b0e87c78e7701e416f2a5d55b03b4e9bf67969a1a604dcbd0c048526a1f8a73e3d7bf7acf27dfb45a69516540c6a84f2afb13f6018223645739e472f2624bd21b2fab4ce6a912b9");


bool valid_pkcs(mpz_class c, int len){
    int k = 0;
    mpz_class last;
    mpz_class m;
    mpz_powm(c.get_mpz_t(), c.get_mpz_t(), d.get_mpz_t(), n.get_mpz_t());
    m = c;
    for(mpz_class t = c; t > 0; t/=256){
        k++;
        last = t % 256;
    }
    if (k != len - 1){
        return false;
    }
    return mpz_class(2) == last;
}

mpz_class ceil_mpz(mpz_class a, mpz_class b){
    mpz_class c = (a + b - 1) / b;
    return c;
}

mpz_class floor_mpz(mpz_class a, mpz_class b){
    mpz_class c = a / b;
    return c;
}

mpz_class attack(mpz_class c, mpz_class e, mpz_class n, int len){
    std::cout << "started attack" << std::endl;
    mpz_class B, B2, B3;
    B = 2;
    mpz_pow_ui(B.get_mpz_t(), B.get_mpz_t(), 8 * (len - 2));
    B2 = 2 * B;
    B3 = 3 * B;

    mpz_class s, pow, c0;
    int oracle_calls = 0;

    if(valid_pkcs(c, len)){
        oracle_calls++;
        s = 1;
    }
    else{
        for(mpz_class t = 1; t < n; t++){
            mpz_powm(pow.get_mpz_t(), t.get_mpz_t(), e.get_mpz_t(), n.get_mpz_t());
            c0 = c * pow;
            c0 %= n;
            oracle_calls++;
            if(valid_pkcs(c0, len)){
                s = t;
                break;
            }
        }
    } 

    mpz_powm(pow.get_mpz_t(), s.get_mpz_t(), e.get_mpz_t(), n.get_mpz_t());
    c0 = c * pow;
    c0 %= n;

    std::vector<std::pair<mpz_class, mpz_class>> Ms;
    Ms.push_back(std::pair<mpz_class, mpz_class>(B2, B3-1));
   
    int rounds = 1;

    mpz_class c1;
    while(true){
        if (Ms.size() >= 2){
            for(mpz_class si = s + 1; si < n; si++){
                mpz_powm(pow.get_mpz_t(), si.get_mpz_t(), e.get_mpz_t(), n.get_mpz_t());
                c1 = c0 * pow;
                c1 %= n;
                oracle_calls++;
                if(valid_pkcs(c1, len)){
                    s = si;
                    break;
                }
            }
        }
        else if (Ms.size() == 1){
            mpz_class a, b;
            a = Ms[0].first;
            b = Ms[0].second;
            bool flag = false;

            mpz_class ri_start = ceil_mpz(2 * (b * s - B2), n);

            for(mpz_class ri = ri_start; ri < n; ri++){
                mpz_class si_start = ceil_mpz(B2 + ri * n, b);
                mpz_class si_end = floor_mpz(B3 - 1 + ri * n, a);

                for(mpz_class si = si_start; si <= si_end; si++){
                    mpz_powm(pow.get_mpz_t(), si.get_mpz_t(), e.get_mpz_t(), n.get_mpz_t());
                    c1 = c0 * pow;
                    c1 %= n;
                    oracle_calls++;
                    if(valid_pkcs(c1, len)){
                        s = si;
                        flag = true;
                        break;
                    }
                }
                if(flag){
                    break;
                }
            }
        }

        std::vector<std::pair<mpz_class, mpz_class>> tmp;
        mpz_class a, b;
        for(int t = 0; t < Ms.size(); t++){
            a = Ms[t].first;
            b = Ms[t].second;

            mpz_class r_lower = ceil_mpz(a * s - B3 + 1, n);
            mpz_class r_upper = floor_mpz(b * s - B2, n);
            for(mpz_class r = r_lower; r <= r_upper; r++){
                mpz_class a1 = ceil_mpz(B2 + r * n, s);
                mpz_class b1 = floor_mpz(B3 - 1 + r * n, s);

                mpz_class newa = std::max(a, a1);
                mpz_class newb = std::min(b, b1);

                if(newa <= newb){
                    tmp.push_back(std::pair<mpz_class, mpz_class>(newa, newb));
                }
            }
        }

        if (tmp.size() > 0){
            Ms = tmp;
        }

        if (Ms.size() == 1){
            a = Ms[0].first;
            b = Ms[0].second;
            if (a == b){
                std::cout << "Finished in " << rounds << " rounds. Oracle calls: " << oracle_calls << ". Modulus length: " << 8 * len << "." << std::endl;
                return a;  // fix that to a * pow(s0, -1, n) % n
            }
        }
        rounds++;
    }
}


//m, c, n, e, p, q, a = 0x206218e8c5e3b527a162ea56184e18012b6b982098bfe86d408d144f7296442186248f37016bc3eb256dfb1ff0a262f991b79cd7749299515f75a1115bff2bf0994d1f0b0d603c2a105a18e9a9910043ded1ed1eb1f242184d31322e001157cd7b3a9fa55519ee21d5973c94cde0d67bf574ebb14e50061626f6261, 0x51af6f1638a957e2946e8a98afff5d1710ab43594b63fc01397720f88e89f54342b9f5eec8eb92b8fb4e381b5cda391b92ea242bea4baa7eb50a53d37bd385b5825a407fe95c5f787bb468f8d7fc0ec1b5d181e14bb790afd4d754ffc2c867c729b714351eb5db86961f7d416a297f02eb38f0ab838991f2e5c1f9f584, 0x8da842199cf73a7ece7e236131c2b522846ec2b1c913a18f122ac30ed2324715447f140152ac3519399e53cd9b671ff2d9c4539ff3f9b4f05dd78e2b592ab86043546735f52a96db45874b3d377fe9ea2b4e05486eed2c47fd79047467b4245827fb1c98551d2de31a1a40826b8035ecb1f3b67cc82eb5783595b9c447, 0x10001, 0xe82ac35e9afe3210e3ba8a863ba9aa91504c97dcc4f53ea32d2228acbba95784ce004757ae7632da6d44f3dc1bb7fb4310c87c8fc8cbb9eedf602646b1265, 0x9c32f124fdb987c8073cca6ee6d572b21ad03be79fbc9aaa1676e751573f38f5a5feb8fcf31af5cfb2efbea2d740d0ab8a68b859eb56cc55c8efe53fe7b3b, 0x206218e8c5e3b527a162ea56184e18012b6b982098bfe86d408d144f7296442186248f37016bc3eb256dfb1ff0a262f991b79cd7749299515f75a1115bff2bf0994d1f0b0d603c2a105a18e9a9910043ded1ed1eb1f242184d31322e001157cd7b3a9fa55519ee21d5973c94cde0d67bf574ebb14e50061626f6261 
            
int main(){
    std::cout << m << std::endl;
    std::cout << attack(c,e, n, 125) << std::endl;
}
