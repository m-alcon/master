#include "kd_tree.h"

void print_point(const Point &p) {
    cout << "(";
    cout << p[0];
    for (int j = 1; j < p.size(); ++j)
        cout << "," << p[j];
    cout << ")" << endl;
}

void print_point_vector(const PointVector &v) {
    for (int i = 0; i < v.size(); ++i) {
        print_point(v[i]);
    }
}

Point KDTree::median(const uint &axis, PointVector v) {
    uint median_pos;
    if (v.size() % 2 == 0) 
        median_pos = v.size()/2;
    else
        median_pos = (v.size()-1)/2;
    auto comp = [&](Point x, Point y) {return x[axis] < y[axis];};
    sort(v.begin(), v.end(), comp);
    print_point_vector(v);
    return v[median_pos];
}


KDTree::KDTree (const uint &dim) {

}

KDTree::KDTree (const uint &dim, const PointVector &v) {
    this->dim = dim;
    print_point(KDTree::median(1,v));
}

KDTree* KDTree::build_default (const uint &i, const PointVector &v) {

}

int main() {
    KDTree (0, {{5,2},{9,5},{2,6},{4,3},{3,4},{6,1}});
}