#include "utils.h"

class KDTree {
    public:
        KDTree (const uint &dim, Data* data);
        friend ostream & operator << (std::ostream & out, const KDTree & kdt);
        friend ostream & operator << (std::ostream & out, const KDTree* kdt);

        Point search(const Point &p);
        Point limited_search(int &n, const Point &p);

    private:
        uint dim, axis, location;
        KDTree* left;
        KDTree* right;
        Data* data;

        KDTree (const uint &dim);
        static IPoint median(const uint &axis, const PointVector &v);
        static IPoint qselect(const uint &k, const uint &axis, const PointVector &v);
        static float distance(const Point &p, const Point &q);
        void recursive_search(float &best_distance, Point &best_p, int &n, const Point &p);
        void explore_children(float &best_distance, Point &best_p, const Point &current_p, int &n, const Point &p);
        void build_standard (const uint &dim, Data* data, const PointVector &v);
        bool check_dimension(const PointVector &v);
        
};