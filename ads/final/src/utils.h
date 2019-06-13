#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <math.h>   
using namespace std;

typedef vector<float> Point;

struct IPoint {
    Point point;
    uint idx;
};

typedef vector<IPoint> PointVector;

struct Data {
    PointVector v;
    vector<float> hv_idx; //High variance indexes
};

ostream & operator << (std::ostream & out, const Point & p) {
    out << "(";
    out << p[0];
    for (int j = 1; j < p.size(); ++j)
        out << "," << p[j];
    out << ")";
    return out;
}

ostream & operator << (std::ostream & out, const PointVector & v) {
    for (int i = 0; i < v.size(); ++i) {
        out << (v[i].point);
    }
    return out;
}

PointVector generate_point_vector(const vector<Point> v) {
    PointVector pv = PointVector (v.size());
    for (int i = 0; i < v.size(); ++i) {
        IPoint ip;
        ip.idx = i;
        ip.point = v[i];
        pv[i] = ip;
    }
    return pv;
}

vector<float> compute_high_variance_idx(const PointVector &v) {
    
}