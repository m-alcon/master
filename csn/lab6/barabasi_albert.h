#include "graph.h"
#include <random>

class BarabasiAlbert {
    private:
        void start_random_cycle (Graph &graph);
        void start_random_cycle_stubs (Graph &graph, Vector &stubs);
        random_device device;
        mt19937 generator;
    public:
        uint n0, m0;
        BarabasiAlbert (const uint &n0_, const uint &m0_);
        void growth_preferential (const uint &t_max);
        void growth_random (const uint &t_max);
        void nogrowth_preferential (const uint &t_max);
};