#include "rkd_tree.h"

RKDTree::RKDTree (const int &n, const int &m, const int &k, const PointVector &v) {
    this->n = n;
    this->m = m;
    this->k = k;
    this->data.v = pointvector_to_ipointvector(v);
    this->data.hv_idx = compute_high_variance_idx(this->k, this->data.v); //TODO
    for (uint id : this->data.hv_idx) {
        cout << id << " ";
    }
    cout << endl;
    this->trees = TreeVector (this->m);

    for (KDTree t : this->trees) {
        t = KDTree(this->data.v[0].point.size(), &this->data);
    }
}

Point RKDTree::search(const Point &p) {
    auto comp = [&](ITree t1, ITree t2) {
        return t1.distance > t2.distance;
    };
    priority_queue<ITree, vector<ITree>, function<bool(ITree, ITree)>> q(comp);
    for (int i = 0; i < this->trees.size(); ++i) {
        ITree t;
        t.tree = &trees[i];
        t.distance = KDTree::distance(t.tree->current_point(), p);
        q.push(t);
    }
    int n = this->n;
    float best_distance = 0;

    while (n > 0) {
        --n;
    }

}

void RKDTree::recursive_search(float &best_distance, Point &best_p, int &n, const Point &p) {

}

