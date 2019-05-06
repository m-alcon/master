#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>
#include <math.h> 
#include <vector>
#include <fstream>

#define THREADS 4
#define MAX_DEPTH 5

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
      BoolVarArray circuit_bool(*this, pow(2,depth+1)-1, false, true);
      constraint_creation(0, 0, truth_idx, circuit_bool);
      rel(*this, circuit_bool[0] == ((bool)truth_table[truth_idx]));
    }

    branch(*this, circuit, INT_VAR_DEGREE_MAX(), INT_VALUES_MAX()); // CAREFUL
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

  BoolVar node_bool(const int & row, const int & col, const BoolVarArray &circuit_bool) const {
    if (col >= pow(2,row))
      cerr << "ERR: Trying to access an invalid node." << endl;
    return circuit_bool[(pow(2,row)-1)+col];
  }

  bool is_bit_up(const unsigned int &bit_pos, const int &number) const {
    return ((unsigned int) pow(2, bit_pos) & number) != 0;
  }

  void constraint_creation(const int &row, const int &col, const int &truth_idx, BoolVarArray &circuit_bool) {
    IntVar root = node(row, col);
    BoolVar root_bool = node_bool(row, col, circuit_bool);
    if (row == depth) {
      // NOR gates on leaves are not allowed
      rel(*this, (root >= 0));
    }
    else {
      constraint_creation(row+1, 2*col, truth_idx, circuit_bool);
      constraint_creation(row+1, 2*col+1, truth_idx, circuit_bool);
      IntVar left = node(row+1,2*col);
      IntVar right = node(row+1, 2*col+1);
      BoolVar left_bool = node_bool(row+1, 2*col, circuit_bool);
      BoolVar right_bool = node_bool(row+1, 2*col+1, circuit_bool);
      // Force childs of root to be 0 if root is not a NOR gate 
      rel(*this, (root >= 0) >> (left == 0 && right == 0));
      // Force non-symetry
      rel(*this, (root == -1) >> (left >= right));
      rel(*this, ((root == -1) && (left > 0 || right > 0)) >> (left > right));
      // Link -1 with the value according to the functionality of a NOR gate
      rel(*this, (root == -1) >> (root_bool == !(left_bool || right_bool)));
    }
    // Link 0 with value 0
    rel(*this, (root == 0) >> !root_bool);
    // Link each variable with its value according to truth_idx (idx of the row of the truth table)
    for (int i = 1; i <= n; ++i) {
      if (is_bit_up(n-i,truth_idx))
        rel(*this, (root == i) >> root_bool);
      else
        rel(*this, (root == i) >> !root_bool);
    }

    // if (row > 0) {
    //   IntVar father = node(row-1, (col-col%2)/2);
    //   rel(*this, (root != 0) >> (father == -1));
    // }
  }

  void print_circuit(const int &row, const int &col, const int &id, int &remaining_id) const {
    int code = node(row,col).val();
    cout << id << " " << code << " ";
    if (code == -1) {
      int left_id = remaining_id+1;
      int right_id = remaining_id+2;
      cout << left_id << " " << right_id << endl;
      remaining_id += 2;
      print_circuit(row+1, 2*col, left_id, remaining_id);
      print_circuit(row+1, 2*col+1, right_id, remaining_id);
    }
    else {
      cout << 0 << " " << 0 << endl;
    }
  }

  void print() const {
    cout << n << endl;
    for (int i = 0; i < truth_table.size(); ++i)
      cout << truth_table[i] << endl;
    cout << depth << " " << size() << endl;
    int remaining_id = 1;
    print_circuit(0, 0, remaining_id, remaining_id);
    print_cerr();
  }

  void print_cerr() const {
    cerr << circuit << endl;
  }

  virtual void constrain(const Space& _c) {
    const NOR_Circuit& c = static_cast<const NOR_Circuit&>(_c);
    count(*this, circuit, -1, IRT_LE, c.size());
  }

};

vector<int> read_input() {
  int n;
  cin >> n;
  vector<int> truth_table(pow(2,n));
  for (int i = 0; i < pow(2,n); ++i)
    cin >> truth_table[i];
  return truth_table;
}

int main(int argc, char* argv[]) {
  try {
    Search::Options options;
    if (argc > 1) {
       options.threads = atoi(argv[1]);
    }
    else {
      options.threads = THREADS;
    }
    vector<int> truth_table = read_input();
    for (int depth = 0; depth <= MAX_DEPTH; ++depth) {
      NOR_Circuit* mod = new NOR_Circuit(truth_table, depth);
      BAB<NOR_Circuit> e(mod,options);
      delete mod;
      NOR_Circuit *s, *sant;
      sant = e.next();
      if (sant != NULL) {
        while (s = e.next()) {
          delete sant; 
          sant = s;
          sant->print_cerr();
        }
        cerr << "Solution found with depth " << depth << "." << endl;
        sant->print();
        delete sant;
        break;
      }
      cerr << "No solution found with depth " << depth << "." << endl;
    }
  }
  catch (Exception e) {
    cerr << "Gecode exception: " << e.what() << endl;
    return 1;
  }
  return 0;
}
