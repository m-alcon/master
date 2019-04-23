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
  NOR_Circuit(vector<int> t, int d) : n(t.size()), truth_table(t), depth(d), circuit(*this, pow(2,depth+1)-1, -2, n) {
    // Not NOR
    // for (int j = 0; j < N; ++j) {
    //   BoolVarArgs v(N);
    //   for (int i = 0; i < N; ++i) 
    //     v[i] = queen(i, j);
    //   linear(*this, v, IRT_LQ, 1);
    // }
    //linear(*this, circuit, IRT_EQ, n); 
    branch(*this, circuit, INT_VAR_NONE(), INT_VAL_MIN()); // CAREFUL
  }

  NOR_Circuit(NOR_Circuit& c) : Space(c) {
    truth_table = c.truth_table;
    for (int i = 0; i <= n; ++i)
      circuit[i].update(*this, c.circuit[i]);
  }

  virtual Space* copy() {
    return new NOR_Circuit(*this);
  }

  IntVar node(const int & row, const int & col) {
    if (col >= pow(2,row))
      cout << "ERR: Trying to access an invalid node." << endl;
    return circuit[(pow(2,row)-1)+col];
  }

  void analyze(const int & row, const int & col) {
    if (row+1 > depth) {
    }
    else {
      node(row,col);
      analyze(row+1,2*col);
      analyze(row+1,2*col+1);
    }
    
  }

  void print() const {
    cout << "Need implementation." << endl;
    cout << circuit << endl;
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
