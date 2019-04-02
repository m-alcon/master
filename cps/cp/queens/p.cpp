#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>

using namespace Gecode;

class Queens : public Space {
protected:
  BoolVarArray board;
  int N;
public:
  Queens(int n) : N(n), board(*this, n*n, 0, 1) {
    // At most 1 queen per column
    for (int j = 0; j < N; ++j) {
      BoolVarArgs v(N);
      for (int i = 0; i < N; ++i) 
        v[i] = queen(i, j);
      linear(*this, v, IRT_LQ, 1);
    }
    // At most 1 queen per row
    for (int i = 0; i < N; ++i) {
      BoolVarArgs v(N);
      for (int j = 0; j < N; ++j) 
        v[j] = queen(i, j);
      linear(*this, v, IRT_LQ, 1);
    }
    // At most 1 queen per column right diagonal
    for (int j = 0; j < N; ++j) {
      BoolVarArgs v(N-j);
      for (int step = 0; j+step < N; ++step) {
        v[step] = queen(step, j+step);
      }
      linear(*this, v, IRT_LQ, 1);
    }
    // At most 1 queen per row right diagonal
    for (int i = 1; i < N; ++i) {
      BoolVarArgs v(N-i);
      for (int step = 0; i+step < N; ++step) {
        v[step] = queen(i+step, step);
      }
      linear(*this, v, IRT_LQ, 1);
    }
    // At most 1 queen per column left diagonal
    for (int j = 0; j < N; ++j) {
      BoolVarArgs v(j+1);
      for (int step = 0; j-step >= 0; ++step) {
        v[step] = queen(step, j-step);
      }
      linear(*this, v, IRT_LQ, 1);
    }
    // At most 1 queen per row left diagonal
    for (int i = 1; i < N; ++i) {
      BoolVarArgs v(N-i);
      for (int step = 0; i+step < N; ++step) {
        v[step] = queen(i+step, N-1-step);
      }
      linear(*this, v, IRT_LQ, 1);
    }
    linear(*this, board, IRT_EQ, N);
    branch(*this, board, BOOL_VAR_NONE(), BOOL_VAL_MAX());
  }
  Queens(Queens& q) : Space(q) {
    board.update(*this, q.board);
  }
  virtual Space* copy() {
    return new Queens(*this);
  }
  void print(int n) const {
    for (int i = 0; i < n; ++i) {
      for (int j = 0; j < n; ++j) {
        std::cout << (board[i*n+j].val() ? "X" : ".");
      }
      std::cout << std::endl;
    }
  }
  BoolVar queen(int i, int j) const {
    return board[i*N+j];
  }

};

int main(int argc, char* argv[]) {
  if (argc < 2) {
    std::cout << argv[0] <<" N\n\tN:\tSpecify the size of the board (NxN)." << std::endl;
    return -1;
  }
  int n = atoi(argv[1]);
  Queens* q = new Queens(n);
  DFS<Queens> e(q);
  delete q;
  if (Queens* s = e.next()) {
    s->print(n); delete s;
  }
}
