#include "graph.h"
#include <random>

class BarabasiAlbert {
    private:
        uint n0, m0;
        void start_random_graph(Graph &graph, Vector &stubs);
        random_device device;
        mt19937 generator;
    public:
        BarabasiAlbert (const uint &n0_, const uint &m0_): n0(n0_), m0(m0_), generator(device()) {}
        void growth_preferential(const uint &t);
        void growth_random();
        void nogrowth_preferential();
};