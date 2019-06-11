#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

typedef vector<float> Point;
typedef vector<Point> PointVector;

class KDTree {
    public:
        KDTree (const uint &dim);
        KDTree (const uint &dim, const PointVector &v);
        KDTree* build_default (const uint &i, const PointVector &v);

    private:
        uint dim;
        float location;
        KDTree* left;
        KDTree* right;

        static Point median(const uint &axis, PointVector v);
};