#include "kd_tree.h"

typedef vector<KDTree> TreeVector;

class RKDTree {
    public:
        RKDTree (const int &n, const int &m, const vector<Point> &v);

        Point search (const Point &p);
    private:
        // n = limitation of searched nodes, m = limitation of trees
        int n, m;
        TreeVector trees;
        Data data;

        void build_trees ();
};