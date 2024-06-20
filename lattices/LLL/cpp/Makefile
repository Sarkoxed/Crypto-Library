.PHONY: default;
default: all

all: Babai LLL

debug: BabaiD LLLD

LLL: lattice_attacks.cpp lattice_attacks.hpp main_LLL.cpp
	g++ -lgmp -lgmpxx lattice_attacks.cpp main_LLL.cpp -o LLL.out
Babai: lattice_attacks.cpp lattice_attacks.hpp Babai_main.cpp
	g++ -lgmp -lgmpxx lattice_attacks.cpp Babai_main.cpp -o Babai.out

LLLD: lattice_attacks.cpp lattice_attacks.hpp main_LLL.cpp
	g++ -lgmp -lgmpxx lattice_attacks.cpp main_LLL.cpp -o LLL.out -g -ggdb
BabaiD: lattice_attacks.cpp lattice_attacks.hpp Babai_main.cpp
	g++ -lgmp -lgmpxx lattice_attacks.cpp Babai_main.cpp -o Babai.out -g -ggdb

cleam:
	rm *.out
