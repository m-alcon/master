#include "utils.h"

ostream & operator << (std::ostream & out, const Point & p) {
    out << "(";
    if (!p.empty()) {
        out << p[0];
        for (int j = 1; j < p.size(); ++j)
            out << "," << p[j];
    }
    out << ")";
    return out;
}

ostream & operator << (std::ostream & out, const IPoint & p) {
    out << "(";
    if (!p.point.empty()) {
        out << p.point[0];
        for (int j = 1; j < p.point.size(); ++j)
            out << "," << p.point[j];
    }
    out << ")";
    return out;
}

ostream & operator << (std::ostream & out, const IPointVector & v) {
    for (int i = 0; i < v.size(); ++i) {
        out << (v[i].point);
    }
    return out;
}

ostream & operator << (std::ostream & out, const PointVector & v) {
    for (int i = 0; i < v.size(); ++i) {
        out << (v[i]);
    }
    return out;
}

IPointVector pointvector_to_ipointvector(const PointVector v) {
    IPointVector pv = IPointVector (v.size());
    for (int i = 0; i < v.size(); ++i) {
        IPoint ip;
        ip.idx = i;
        ip.point = v[i];
        pv[i] = ip;
    }
    return pv;
}

vector<float> variance(const IPointVector &v) {
    vector<float> axis_mean (v[0].point.size());
    for (IPoint p : v) {
        for (int i = 0; i < p.point.size(); ++i) {
            axis_mean[i] += p.point[i];
        }
    }
    for (int i = 0; i < axis_mean.size(); ++i) {
        axis_mean[i] /= v.size();
    }
    vector<float> axis_variance (v[0].point.size());
    for (IPoint p : v) {
        for (int i = 0; i < p.point.size(); ++i) {
            axis_variance[i] += pow(p.point[i] - axis_mean[i], 2);
        }
    }
    for (int i = 0; i < axis_mean.size(); ++i) {
        axis_variance[i] /= v.size();
    }
    return axis_variance;
}

vector<uint> compute_high_variance_idx(const uint &k, IPointVector v) {
    if (v.empty())
        return vector<uint> (1,0);
    vector<float> var = variance(v);
    uint aux_k = k;
    if (k > v[0].point.size())
        aux_k = v[0].point.size();
    vector<uint> idxs (aux_k);
    iota(idxs.begin(), idxs.end(), 0);
    sort(idxs.begin(), idxs.end(), [var](int i, int j) {return var[i] > var[j];});
    return vector<uint> (idxs.begin(), idxs.begin() + aux_k);
}