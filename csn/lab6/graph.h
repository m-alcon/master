#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
using namespace std;

typedef vector<uint> Vector;
typedef vector<Vector> Matrix;

class Edge {
    public:
        uint u, v;
        Edge ();
        Edge (const uint &u_, const uint &v_)
            : u(u_), v(v_) {}
        bool operator == (const Edge& e) const;
};

class Graph {
    private:
        vector<Edge> edges;
        Matrix adjacency;
    public:
        Graph (const uint &N);
        uint n_vertices();
        uint n_edges();
        void write_edges(ostream &output);
        
        Vector degree_sequence();
        uint create_node();
        void add_edge(const uint &u, const uint &v);

};