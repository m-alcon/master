/*
 *  Authors:
 *    Christian Schulte <schulte@gecode.org>
 *
 *  Copyright:
 *    Christian Schulte, 2008-2013
 *
 *  Permission is hereby granted, free of charge, to any person obtaining
 *  a copy of this software, to deal in the software without restriction,
 *  including without limitation the rights to use, copy, modify, merge,
 *  publish, distribute, sublicense, and/or sell copies of the software,
 *  and to permit persons to whom the software is furnished to do so, subject
 *  to the following conditions:
 *
 *  The above copyright notice and this permission notice shall be
 *  included in all copies or substantial portions of the software.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 *  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 *  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 *  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 *  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 *  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 *  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 */

#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>

using namespace Gecode;

class Queens : public Space {
protected:
  IntVarArray board;
public:
  Queens(int n) : board(*this, n*n, 0, 1) {
    branch(*this, board, INT_VAR_SIZE_MIN(), INT_VAL_MIN());
  }
  Queens(Queens& q) : Space(q) {
    board.update(*this, q.board);
  }
  virtual Space* copy() {
    return new Queens(*this);
  }
  void print(void) const {
    std::cout << board << std::endl;
  }
};

int main(int argc, char* argv[]) {
  if (argc < 1) {
	std::cout << "./" << argv[0] <<" N\n\tN:\tSpecify the size of the board (NxN)." << std::endl;
	return -1;
  }
  Queens* q = new Queens(atoi(argv[1]));
  DFS<Queens> e(q);
  delete q;
  while (Queens* s = e.next()) {
    s->print(); delete s;
  }
}
