#include "graph.h"
#include <random>

class BarabasiAlbert {
    private:
        uint n0;
        void start_random_graph(Graph &graph, Vector &stubs);
        random_device device;
        mt19937 generator;
    public:
        BarabasiAlbert(const uint &n0_): n0(n0_), generator(device()) {}
        void growth_preferential(const uint &t, const uint &m0);
        void growth_random();
        void nogrowth_preferential();
};