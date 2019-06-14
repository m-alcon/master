#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <math.h>   

using namespace std;

typedef vector<float> Point;
typedef vector<Point> PointVector;

class KDTree {
    public:
        KDTree (const uint &dim);
        KDTree (const uint &dim, const PointVector &v);
        friend ostream & operator << (std::ostream & out, const KDTree & kdt);
        friend ostream & operator << (std::ostream & out, const KDTree* kdt);

        Point search(const Point &p);
        Point limited_search(const uint &n, const Point &p); //TODO

    private:  
        Point location;
        KDTree* left;
        KDTree* right;
        uint dim, axis; 

        static Point median(const Point &axis, PointVector v);
        static uint qselect(const uint &k, const uint &axis, PointVector v);
        static float distance(const Point &p, const Point &q);
        void recursive_search(float &best_distance, Point &best_p, const Point &p);
        void build_standard (const PointVector &v);
        bool check_dimension(const PointVector &v);
        
};