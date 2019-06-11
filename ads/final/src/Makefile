CXX  = g++ -std=c++11
OBJ = ./
BIN = ./

SRC = $(wildcard *.cc)
TAR = $(SRC:.cc=)

.PHONY: all clean

all: $(TAR)

%: %.cc
	$(CXX) -c $^ -o $(OBJ)$@.o
	$(CXX) -o $(BIN)$@ $(OBJ)$@.o
	rm $(OBJ)$@.o

clean:
	rm -rf $(OBJ)*.o $(TAR)