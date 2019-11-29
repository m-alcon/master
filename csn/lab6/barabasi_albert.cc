#include "barabasi_albert.h"

BarabasiAlbert::BarabasiAlbert (const uint &n0_, const uint &m0_)
    : n0(n0_), m0(m0_), generator(device()) {
    if (m0 > n0)
        cerr << "WARNING: m0 > n0." << endl;
}

void BarabasiAlbert::start_random_cycle (Graph &graph) {
    Vector order = Vector(graph.n_vertices());

    for (uint i = 0; i < graph.n_vertices(); ++i)
        order[i] = i;
    shuffle(order.begin(), order.end(), generator);

    for (uint i = 1; i < order.size(); ++i) {
        graph.add_edge(order[i-1], order[i]);
    }
    graph.add_edge(order[order.size()-1], order[0]);
}

void BarabasiAlbert::start_random_cycle_stubs (Graph &graph, Vector &stubs) {
    Vector order = Vector(graph.n_vertices());

    for (uint i = 0; i < graph.n_vertices(); ++i)
        order[i] = i;
    shuffle(order.begin(), order.end(), generator);

    for (uint i = 1; i < order.size(); ++i) {
        graph.add_edge(order[i-1], order[i]);
        stubs.push_back(order[i-1]);
        stubs.push_back(order[i]);
    }
    graph.add_edge(order[order.size()-1], order[0]);
    stubs.push_back(order[order.size()-1]);
    stubs.push_back(order[0]);
}

void BarabasiAlbert::growth_preferential (const uint &t_max) {
    Graph graph(n0);
    Vector stubs(0);
    start_random_cycle_stubs(graph, stubs);
    string main_file = "data/gp_" + to_string(n0) + "_" + to_string(m0) + "_" + to_string(t_max);

    for (uint t = 1; t < t_max; ++ t) {
        uint min_m0 = min(m0, graph.n_vertices());
        uint node = graph.create_node();
        for (uint i = 0; i < min_m0; ++i) {
            uniform_int_distribution<int> distribution(0,stubs.size()-1);
            uint idx = distribution(generator);
            while (graph.has_connection(node, stubs[idx]))
                idx = distribution(generator);
            graph.add_edge(stubs[idx], node);
            stubs.push_back(stubs[idx]);
            stubs.push_back(node);
        }
        if (t == 1) {
            ofstream output(main_file + "_ts_1.txt");
            graph.write_limited_degree_sequence(n0+1, output);
            output.close();
        } else if (t == 10) {
            ofstream output(main_file + "_ts_2.txt");
            graph.write_limited_degree_sequence(n0+1, output);
            output.close();
        } else if (t == 100) {
            ofstream output(main_file + "_ts_3.txt");
            graph.write_limited_degree_sequence(n0+1, output);
            output.close(); 
        } else if (t == 1000) {
            ofstream output(main_file + "_ts_4.txt");
            graph.write_limited_degree_sequence(n0+1, output);
            output.close();
        }
    }
    ofstream output(main_file + "_ds.txt");
    graph.write_degree_sequence(output);
    output.close();
}

void BarabasiAlbert::growth_random (const uint &t_max) {
    Graph graph(n0);
    start_random_cycle(graph);
    string main_file = "data/gr_" + to_string(n0) + "_" + to_string(m0) + "_" + to_string(t_max);

    for (uint t = 1; t < t_max; ++ t) {
        uint min_m0 = min(m0, graph.n_vertices());
        uint new_node = graph.create_node();
        for (uint i = 0; i < min_m0; ++i) {
            uniform_int_distribution<int> distribution(0, graph.n_vertices()-1);
            uint old_node = distribution(generator);
            while (graph.has_connection(new_node, old_node))
                old_node = distribution(generator);
            graph.add_edge(old_node, new_node);
        }

        if (t == 1) {
            ofstream output(main_file + "_ts_1.txt");
            graph.write_limited_degree_sequence(n0+1, output);
            output.close();
        } else if (t == 10) {
            ofstream output(main_file + "_ts_2.txt");
            graph.write_limited_degree_sequence(n0+1, output);
            output.close();
        } else if (t == 100) {
            ofstream output(main_file + "_ts_3.txt");
            graph.write_limited_degree_sequence(n0+1, output);
            output.close(); 
        } else if (t == 1000) {
            ofstream output(main_file + "_ts_4.txt");
            graph.write_limited_degree_sequence(n0+1, output);
            output.close();
        }
    }
    ofstream output(main_file + "_ds.txt");
    graph.write_degree_sequence(output);
    output.close();
}

void BarabasiAlbert::nogrowth_preferential (const uint &t_max) {
    Graph graph(n0);
    Vector stubs(0);
    start_random_cycle_stubs(graph, stubs);
    string main_file = "data/np_" + to_string(n0) + "_" + to_string(m0) + "_" + to_string(t_max);

    uniform_int_distribution<int> distribution(0, n0-1);
    for (uint t = 1; t < t_max; ++ t) {
        uint node = distribution(generator);
        uint min_m0 = min(m0, n0-1-graph.degree(node));
        for (uint i = 0; i < min_m0; ++i) {
            uniform_int_distribution<int> stub_distribution(0, stubs.size()-1);
            uint idx = stub_distribution(generator);
            while (graph.has_connection(node, stubs[idx]))
                idx = stub_distribution(generator);
            graph.add_edge(stubs[idx], node);
            stubs.push_back(stubs[idx]);
            stubs.push_back(node);
        }
        if (t == 1) {
            ofstream output(main_file + "_ts_1.txt");
            graph.write_degree_sequence(output);
            output.close();
        } else if (t == 10) {
            ofstream output(main_file + "_ts_2.txt");
            graph.write_degree_sequence(output);
            output.close();
        } else if (t == 100) {
            ofstream output(main_file + "_ts_3.txt");
            graph.write_degree_sequence(output);
            output.close(); 
        } else if (t == 1000) {
            ofstream output(main_file + "_ts_4.txt");
            graph.write_degree_sequence(output);
            output.close();
        }
    }
    ofstream output(main_file + "_ds.txt");
    graph.write_degree_sequence(output);
    output.close();
}

void print_usage() {
    cerr << "usage: ./barabasi_albert type n0 m0 t_max" << endl;
    cerr << "\ttype: all gp gr np" << endl;
}

int main (int argc, char *argv[]) {
    if (argc != 5) {
        cerr << "ERROR: some parameters are not specified." << endl;
        print_usage();
        return 1;
    }
    string type = argv[1];
    int n0 = atoi(argv[2]);
    int m0 = atoi(argv[3]);
    int t_max = atoi(argv[4]);

    BarabasiAlbert ba (n0, m0);
    if (type == "all") {
        ba.growth_preferential(t_max);
        ba.growth_random(t_max);
        ba.nogrowth_preferential(t_max);
    } else if (type == "gp") {
        ba.growth_preferential(t_max);
    } else if (type == "gr") {
        ba.growth_random(t_max);
    } else if (type == "np") {
        ba.nogrowth_preferential(t_max);
    } else {
        cerr << "ERROR: Non-defined type." << endl;
        print_usage();
    }    
}