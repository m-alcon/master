GCC=g++ --std=c++11

all: graph barabasi_albert

graph: graph.cc graph.h
	$(GCC) -c graph.cc

barabasi_albert: graph.o barabasi_albert.h barabasi_albert.cc
	$(GCC) -c barabasi_albert.cc
	$(GCC) -o barabasi_albert.exe barabasi_albert.o graph.o

clean:
	rm *.o *.exe