#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
using namespace std;

typedef vector<uint> Vector;
typedef vector<Vector> Matrix;

class Graph {
    private:
        Matrix adjacency;
    public:
        Graph (const uint &N);
        uint n_vertices ();
        uint degree (const uint &node);
        void write_degree_sequence (ostream &output);
        void write_limited_degree_sequence (uint lim, ostream &output);

        uint create_node ();
        void add_edge (const uint &u, const uint &v);

        bool has_connection (const uint &u, const uint &v);

};