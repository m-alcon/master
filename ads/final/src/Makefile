CXX  = g++ -std=c++11
OBJ = ../obj/
BIN = ./

SRC = $(wildcard *.cc)
TAR = $(SRC:.cc=.o)

.PHONY: all clean

all: $(TAR) experiment

%.o: %.cc
	$(CXX) -c $^ -o $(OBJ)$@

experiment: utils.o kd_tree.o rkd_tree.o experiment.o
	$(CXX) -O3 -o $(BIN)experiment $(OBJ)experiment.o $(OBJ)utils.o $(OBJ)kd_tree.o $(OBJ)rkd_tree.o

clean:
	rm -rf $(OBJ)*.o $(TAR)
