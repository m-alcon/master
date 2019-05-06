CXX  = g++ -std=c++11
DIR  = /usr/local
LIBS = -lgecodedriver    -lgecodesearch  \
       -lgecodeminimodel -lgecodeint     \
       -lgecodekernel    -lgecodesupport
OBJ = ./
BIN = ./

SRC = $(wildcard *.cc)
TAR = $(SRC:.cc=)

.PHONY: all clean

all: $(TAR)

init_directories:
	mkdir -p $(OBJ) 
	mkdir -p $(BIN) 

%: %.cc
	$(CXX) -I$(DIR)/include -c $^ -o $(OBJ)$@.o
	$(CXX) -L$(DIR)/lib -o $(BIN)$@ $(OBJ)$@.o $(LIBS)
	rm $(OBJ)$@.o

clean:
	rm -rf $(OBJ)*.o $(TAR)
