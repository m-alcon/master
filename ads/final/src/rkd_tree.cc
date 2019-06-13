#include "rkd_tree.h"

RKDTree::RKDTree (const int &n, const int &m, const vector<Point> &v) {
    this->n = n;
    this->m = m;
    Data data;
    data.v = generate_point_vector(v);
    data.hv_idx = compute_high_variance_idx(data.v); //TODO
    RKDTree::build_trees(); //TODO
}

void RKDTree::build_trees() {

}

