CXX  = g++ -std=c++11
DIR  = /usr/local
LIBS = -lgecodedriver    -lgecodesearch  \
       -lgecodeminimodel -lgecodeint     \
       -lgecodekernel    -lgecodesupport
OBJ = ./obj/
BIN = ./bin/

SRC = $(wildcard *.cpp)
TAR = $(SRC:.cpp=)

.PHONY: all clean

all: $(TAR)

init_directories:
	mkdir -p $(OBJ) 
	mkdir -p $(BIN) 

%: %.cpp
	$(CXX) -I$(DIR)/include -c $^ -o $(OBJ)$@.o
	$(CXX) -L$(DIR)/lib -o $(BIN)$@ $(OBJ)$@.o $(LIBS)

clean:
	rm -rf $(OBJ) $(BIN)
