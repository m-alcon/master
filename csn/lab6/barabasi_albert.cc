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

    graph.write_edges(cout);
}

void BarabasiAlbert::growth_preferential(const uint &t_max, const uint &m0) {
    Graph graph(n0);
    Vector stubs;
    start_random_graph (graph, stubs);
    uint s0 = stubs.size();

    for (uint t = 1; t < t_max; ++ t) {
        uint new_node = graph.create_node();
        for (uint i = 0; i < m0; ++i) {
            uniform_int_distribution<int> distribution(0,stubs.size());
            uint stub_node = distribution(generator);
            graph.add_edge(stub_node, new_node);
            stubs.push_back(stub_node);
            stubs.push_back(new_node);            
        }
    }

    graph.write_edges(cout);
}

int main() {
    BarabasiAlbert ba (5);
    ba.growth_preferential(10, 1);
}