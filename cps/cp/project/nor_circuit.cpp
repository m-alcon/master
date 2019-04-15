#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>
#include <math.h> 
#include <vector>
#include <fstream>

#define MAX_DEPTH 1

using namespace std;
using namespace Gecode;

class NOR_Circuit : public Space {
protected:
  vector<int> truth_table;
  IntVarArray circuit;
  IntVar size;
  int n, depth;
public:
  NOR_Circuit(vector<int> t, int d) : n(t.size()), truth_table(t), depth(d), circuit(*this, n*depth, 0, 1) {
    // At most 1 queen per column
    // for (int j = 0; j < N; ++j) {
    //   BoolVarArgs v(N);
    //   for (int i = 0; i < N; ++i) 
    //     v[i] = queen(i, j);
    //   linear(*this, v, IRT_LQ, 1);
    // }
    linear(*this, circuit, IRT_EQ, n);
    //branch(*this, circuit, BOOL_VAR_NONE(), BOOL_VAL_MAX());
  }

  NOR_Circuit(NOR_Circuit& c) : Space(c) {
    c.truth_table;
    circuit.update(*this, c.circuit);
  }

  virtual Space* copy() {
    return new NOR_Circuit(*this);
  }

  void print() const {
    cout << "Need implementation." << endl;
  }

  IntVar queen(int i, int j) const {
    return circuit[i*n+j];
  }

};

vector<int> read_input(string path) {
  ifstream input(path);
  int n;
  input >> n;
  vector<int> truth_table(pow(2,n));
  for (int i = 0; i < pow(2,n); ++i)
    input >> truth_table[i];
  return truth_table;
}

int main(int argc, char* argv[]) {
  if (argc != 2) {
    cout << argv[0] <<" FILE\n\tFILE:\tPath of the input file." << endl;
    return -1;
  }
  vector<int> truth_table = read_input(argv[1]);
  for (int depth = 1; depth <= MAX_DEPTH; ++depth) {
    cout << "Solving with depth = " << depth << "." << endl;
    NOR_Circuit* c = new NOR_Circuit(truth_table,depth);
    //DFS<NOR_Circuit> e(c);
    //delete c;
    //if (NOR_Circuit* s = e.next()) {
    //  s->print(); delete s;
    //} 
  }
  cout << endl << "WAR: Depth should start at 0, now starts at 1." << endl;
}
