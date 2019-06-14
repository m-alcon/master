#include <queue>
#include <functional>
#include "kd_tree.h"

typedef vector<KDTree> TreeVector;

struct ITree {
    KDTree* tree;
    float distance;
};

class RKDTree {
    public:
        RKDTree (const int &n, const int &m, const int &k, const PointVector &v);

        Point search (const Point &p);
    private:
        // n = limitation of searched nodes, m = limitation of trees, k = #idxs of high variance
        int n, m, k;
        TreeVector trees;
        Data data;
        void recursive_search(float &best_distance, Point &best_p, int &n, const Point &p);
};