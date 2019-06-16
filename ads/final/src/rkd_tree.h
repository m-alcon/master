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
        int n, m, k;
        Data data;
        
        RKDTree (const int &n, const int &m, const int &k, const PointVector &v);
        static ITree generate_itree(KDTree* t, const Point &p);
        Point search (const Point &p);
        
    private:
        // n = limitation of searched nodes, m = limitation of trees, k = #idxs of high variance
        TreeVector trees;
        
        void recursive_search(float &best_distance, Point &best_p, int &n, const Point &p);
};