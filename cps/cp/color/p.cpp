#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>
#include <fstream>
#include <vector>

using namespace std;
using namespace Gecode;

class Coloring : public Space {
protected:
  int n;
  IntVarArray colors;
public:
  Coloring(const vector<vector<int>>& graph) : n(graph.size()), colors(*this, n, 1, n) {
    // u <-> v
    for (int u = 0; u < n; ++u) {
      for (int i = 0; i < graph[u].size() ; ++i) {
	int v = graph[u][i];
	if (u < v)
	  rel(*this, colors[u] != colors[v]);
      }
    }
    branch(*this, colors, INT_VAR_NONE(), INT_VAL_MIN());
  }
  Coloring(Coloring& c) : Space(c) {
    n = c.n;
    colors.update(*this, c.colors);
  }
  virtual Space* copy() {
    return new Coloring(*this);
  }
  void print() const {
    for (int i = 0; i < n; ++i)
    	cout << colors[i] << endl;
  }

};

int main(int argc, char* argv[]) {
  // READ INPUT
  if (argc < 2) {
    cout << argv[0] <<" input\n\tn:\tNumber of vertices.\n\tm:\tNumber of edges\n\tinput:\tFile describing the problem's graph." << endl;
    return -1;
  }
  ifstream input(argv[1]);
  int n, m;
  input >> n >> m;
  vector<vector<int>> graph(n);
  for (int i = 0; i < m; ++i) {
    int u,v;
    input >> u >> v;
    --u;--v;
    graph[u].push_back(v);
    graph[v].push_back(u);
  }
  // START SOLVER
  Coloring* c = new Coloring(graph);
  DFS<Coloring> e(c);
  delete c;
  if (Coloring* s = e.next()) {
    s->print(); delete s;
  }
}
