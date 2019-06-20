#include "rkd_tree.h"

RKDTree::RKDTree (const int &n, const int &m, const int &k, const PointVector &v) {
    this->n = n;
    this->m = m;
    this->k = k;
    this->data.v = pointvector_to_ipointvector(v);
    this->data.hv_idx = compute_high_variance_idx(this->k, this->data.v); //TODO
    this->trees = TreeVector (this->m);

    for (int i = 0; i < this->m; ++i) {
        this->trees[i] = KDTree(this->data.v[0].point.size(), &this->data);
    }
}

ITree RKDTree::generate_itree(KDTree* t, const Point &p) {
    ITree it;
    it.tree = t;
    if (t != NULL)
        it.distance = KDTree::distance(it.tree->current_point(), p);
    else
        it.distance = -1;
    return it;
}

Point RKDTree::search(const Point &p) {
    auto comp = [&](ITree t1, ITree t2) {
        return t1.distance > t2.distance;
    };
    priority_queue<ITree, vector<ITree>, function<bool(ITree, ITree)>> q(comp);
    for (int i = 0; i < this->trees.size(); ++i) 
        q.push(RKDTree::generate_itree(&trees[i], p));

    int n = this->n;
    float best_distance = -1;
    Point best_point;
    while (n > 0 and !q.empty() and best_distance != 0) {
        ITree t = q.top();
        q.pop();
        if (best_distance == -1 or t.distance < best_distance) {
            best_distance = t.distance;
            best_point = t.tree->current_point();
        }
        if (t.tree->left != NULL)
            q.push(RKDTree::generate_itree(t.tree->left, p));
        if (t.tree->right != NULL)
            q.push(RKDTree::generate_itree(t.tree->right, p));
        --n;
    }
    cout << "Visited nodes:" << this->n - n << endl;
    return best_point;

}

void RKDTree::recursive_search(float &best_distance, Point &best_p, int &n, const Point &p) {

}

