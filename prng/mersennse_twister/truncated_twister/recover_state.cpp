#include <Eigen/Dense>
#include <iostream>

std::ostream& operator<<(std::ostream& out, const std::array<uint8_t, 32>& x){
    for(size_t i = 0; i < 32; i++){
        out << static_cast<uint32_t>(x[i]);
    }
    return out;
}

std::array<uint8_t, 32> i2b(uint32_t x){
    std::array<uint8_t, 32> res;
    for(size_t i = 31; i < 32; i--){
        res[i] = x & 1;
        x >>= 1;
    }
    return res;
}

void shr(std::array<uint8_t, 32>& x, uint32_t n){
    for(size_t i = 31; i < 32; i--){
        if(i < n){
            x[i] = 0;
        }else{
            x[i] = x[i - n];
        }
    }
}

void shl(std::array<uint8_t, 32>& x, uint32_t n){
    for(size_t i = 0; i < 32; i++){
        if(i > 31 - n){
            x[i] = 0;
        }else{
            x[i] = x[i + n];
        }
    }
}

void and_(std::array<uint8_t, 32>)

void twist(std::vector<std::array<uint8_t, 32 * 624>>& state){
    return;
} 


int main(){
    uint32_t a = 99420245;
    auto vec = i2b(a);
    std::cout << vec << std::endl;
    shl(vec, 13);
    std::cout << vec << std::endl;
    shr(vec, 17);
    std::cout << vec << std::endl;
}
