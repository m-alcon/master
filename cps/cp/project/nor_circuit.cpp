#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>
#include <math.h> 
#include <vector>
#include <fstream>

#define MAX_DEPTH 10

using namespace std;
using namespace Gecode;

class NOR_Circuit : public Space {
protected:
  vector<int> truth_table;
  IntVarArray circuit;
  int n, depth;
public:
  NOR_Circuit(vector<int> t, int d) : n(log2(t.size())), truth_table(t), depth(d), circuit(*this, pow(2,d+1)-1, -1, log2(t.size())) {
    for (int truth_idx = 0; truth_idx < t.size(); ++truth_idx) {
      BoolVarArray circuit_bool(*this, pow(2,depth+1)-1, 0,1);
      analyze(0, 0, truth_idx, circuit_bool);
      rel(*this, circuit_bool[0] == ((bool)truth_table[truth_idx]));
    }

    branch(*this, circuit, INT_VAR_NONE(), INT_VAL_MIN()); // CAREFUL
  }

  NOR_Circuit(NOR_Circuit& c) : Space(c) {
    truth_table = c.truth_table;
    n = c.n;
    depth = c.depth;
    circuit.update(*this, c.circuit);
  }

  virtual Space* copy() {
    return new NOR_Circuit(*this);
  }

  int size () const {
    int size = 0;
    for (int i = 0; i < circuit.size(); ++i)
      if (circuit[i].val() == -1)
      	++size;
    return size;
  }

  IntVar node(const int & row, const int & col) const {
    if (col >= pow(2,row))
      cerr << "ERR: Trying to access an invalid node." << endl;
    return circuit[(pow(2,row)-1)+col];
  }

  int node_pos(const int & row, const int & col) {
    if (col >= pow(2,row))
      cerr << "ERR: Trying to access an invalid node." << endl;
    return (pow(2,row)-1)+col;
  }

  bool is_bit_up(const unsigned int &bit_pos, const int &number) {
    return ((unsigned int) pow(2, bit_pos) & number) != 0;
  }

  void analyze(const int &row, const int &col, const int &truth_idx, BoolVarArray &circuit_bool) {
    //cout << row << ", " << col << " = " << node_pos(row,col) << endl;
    IntVar root = node(row,col);
    BoolVar root_bool = circuit_bool[node_pos(row,col)];
    if (row == depth) {
      rel(*this, (root == -1) >> !root_bool);
      rel(*this, (root == 0) >> !root_bool);
      for (int i = 1; i <= n; ++i) {
        rel(*this, (root == i) >> (root_bool == is_bit_up(n-i,truth_idx)));
      }
    }
    else {
      analyze(row+1, 2*col, truth_idx, circuit_bool);
      analyze(row+1, 2*col+1, truth_idx, circuit_bool);
      BoolVar left_bool = circuit_bool[node_pos(row+1,2*col)];
      BoolVar right_bool = circuit_bool[node_pos(row+1, 2*col+1)];
      rel(*this, (root == -1) >> (root_bool == !(left_bool || right_bool)));
      rel(*this, (root == 0) >> !root_bool);
      for (int i = 1; i <= n; ++i) {
        rel(*this, (root == i) >> (root_bool == is_bit_up(n-i,truth_idx)));
      }
    }
  }

  void print_circuit(const int &row, const int &col, const int &id, int &remaining_id) const {
    int code = node(row,col).val();
    cout << id << " " << code;
    if (code == -1) {
      int left_id = remaining_id+1;
      int right_id = remaining_id+2;
      cout << " " << left_id << " " << right_id << endl;
      remaining_id += 2;
      print_circuit(row+1, 2*col, left_id, remaining_id);
      print_circuit(row+1, 2*col+1, right_id, remaining_id);
    }
    else {
      cout << " " << 0 << " " << 0 << endl;
    }
    
  }

  void print() const {
    cout << n << endl;
    for (int i = 0; i < truth_table.size(); ++i) {
      cout << truth_table[i] << endl;
    }
    cout << depth << " " << size() << endl;
    int remaining_id = 1;
    print_circuit(0, 0, remaining_id, remaining_id);
    cerr << circuit << endl;
  }

  virtual void constrain(const Space& _c) {
    const NOR_Circuit& c = static_cast<const NOR_Circuit&>(_c);
    count(*this, circuit, -1, IRT_LE, c.size());
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
  try {
    vector<int> truth_table = read_input(argv[1]);
    for (int depth = 0; depth <= MAX_DEPTH; ++depth) {
      cerr << "Solving with depth = " << depth << "." << endl;
      NOR_Circuit* mod = new NOR_Circuit(truth_table, depth);
      BAB<NOR_Circuit> e(mod);
      delete mod;
      NOR_Circuit *s, *sant;
      sant = e.next();
      if (sant != NULL and (s = e.next())) {
        while (s != NULL) {
          delete sant; 
          sant = s;
          s = e.next();
        }
        sant->print();
        delete sant;
        break;
      }
    }
  }
  catch (Exception e) {
    cerr << "Gecode exception: " << e.what() << endl;
    return 1;
  }
  return 0;
}
