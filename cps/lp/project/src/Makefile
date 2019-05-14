OBJ = ./
BIN = ./

SRC = $(wildcard *.cpp)
TAR = $(SRC:.cpp=)

.PHONY: all clean

all: $(TAR) checker

# init_directories:
# 	mkdir -p $(OBJ) 
# 	mkdir -p $(BIN) 

checker: checker.cc
	$(CCC) $^ -o $@

%: %.cpp
	$(CCC) -c $(CCFLAGS) $^ -o $(OBJ)$@.o
	$(CCC) $(CCFLAGS) $(OBJ)$@.o -o $@ $(CCLNFLAGS)

	rm $(OBJ)$@.o

clean:
	rm -rf $(OBJ)*.o $(TAR)

################################

# Uncomment for CPLEX_Enterprise_Server126
SYSTEM     = x86-64_linux
LIBFORMAT  = static_pic
CPLEXDIR      = /home/malcon/Programs/CPLEX_Studio126/cplex
CONCERTDIR    = /home/malcon/Programs/CPLEX_Studio126/concert

# Uncomment for CPLEX_Studio124
#SYSTEM     = x86-64_sles10_4.1
#LIBFORMAT  = static_pic
#CPLEXDIR      = /home/malcon/Programs/CPLEX_Studio126/cplex
#CONCERTDIR    = /home/malcon/Programs/CPLEX_Studio126/concert

################

CCC = g++

CCOPT = -m64 -O3 -fPIC -fno-strict-aliasing -fexceptions -DNDEBUG -DIL_STD

CPLEXBINDIR   = $(CPLEXDIR)/bin/$(BINDIST)
CPLEXLIBDIR   = $(CPLEXDIR)/lib/$(SYSTEM)/$(LIBFORMAT)
CONCERTLIBDIR = $(CONCERTDIR)/lib/$(SYSTEM)/$(LIBFORMAT)

CCLNFLAGS = -L$(CPLEXLIBDIR) -lilocplex -lcplex -L$(CONCERTLIBDIR) -lconcert -lm -pthread

CONCERTINCDIR = $(CONCERTDIR)/include
CPLEXINCDIR   = $(CPLEXDIR)/include

CCFLAGS = $(CCOPT) -I$(CPLEXINCDIR) -I$(CONCERTINCDIR) 
