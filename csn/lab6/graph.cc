#include "graph.h"

// EDGE CLASS
bool Edge::operator == (const Edge& e) const {
    return (u == e.u and v == e.v) or (u == e.v and v == e.u);
}

// GRAPH CLASS
Graph::Graph (const uint &N) {
    adjacency = Matrix(N, Vector());
}
        
void Graph::write_edges(ostream &output) {
    //output << n_vertices() << " " << n_edges() << endl;
    for (Edge e: edges) {
        output << e.u << " " << e.v << endl; 
    }
}

void Graph::write_degree_sequence(ostream &output) {
    for (uint i = 0; i < adjacency.size(); ++i)
        output << adjacency[i].size() << endl;
}

uint Graph::create_node() {
    adjacency.push_back(Vector());
    return adjacency.size()-1;
}

void Graph::add_edge(const uint &u, const uint &v) {
    edges.push_back(Edge(u,v));
    adjacency[u].push_back(v);
    adjacency[v].push_back(u);
}

uint Graph::n_vertices() {
    return adjacency.size();
}
uint Graph::n_edges() {
    return edges.size();
}
