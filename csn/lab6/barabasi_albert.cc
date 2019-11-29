#include "barabasi_albert.h"

void BarabasiAlbert::start_random_graph(Graph &graph, Vector &stubs) {
    Vector order = Vector(graph.n_vertices());

    for (uint i = 0; i < graph.n_vertices(); ++i)
        order[i] = i;
    shuffle(order.begin(), order.end(), generator);

    for (uint i = 1; i < order.size(); ++i) {
        graph.add_edge(order[i-1], order[i]);
        stubs.push_back(order[i-1]);
        stubs.push_back(order[i]);
    }
}

void BarabasiAlbert::growth_preferential(const uint &t_max) {
    Graph graph(n0);
    Vector stubs(0);
    start_random_graph (graph, stubs);

    for (uint t = 1; t < t_max; ++ t) {
        uint node = graph.create_node();
        Vector aux = stubs; // Used to avoid multi-edges
        for (uint i = 0; i < m0; ++i) {
            uniform_int_distribution<int> distribution(0,aux.size()-1);
            uint idx = distribution(generator);
            graph.add_edge(aux[idx], node);
            stubs.push_back(aux[idx]);
            stubs.push_back(node);
            aux.erase(remove(aux.begin(), aux.end(), aux[idx]), aux.end());
            if (aux.empty()) 
                break;
        }
    }
    //graph.write_edges(cout);
    graph.write_degree_sequence(cout);
}

int main() {
    BarabasiAlbert ba (5, 6);
    ba.growth_preferential(10);
}