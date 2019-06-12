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
        friend ostream & operator << (std::ostream & out, const KDTree & kdt);
        friend ostream & operator << (std::ostream & out, const KDTree* kdt);

        Point location;
        KDTree* left;
        KDTree* right;
        uint dim, axis;

    private:   

        static Point median(const uint &axis, PointVector v);
        static Point qselect(const uint &k, const uint &axis, PointVector v);
        //static KDTree* build_standard (const uint &dim, const PointVector &v);
        void build_standard (const PointVector &v);
        bool check_dimension(const PointVector &v);
};