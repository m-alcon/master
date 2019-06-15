#include <random>
#include "rkd_tree.h"

#define MAX_NUM_VAL 10
#define MAX_SEARCH_LIM 10000
#define NUM_HIGH_VAR 16
#define SIZE 100000
#define DIMENSIONS 128

Point generate_point(const uint &dim, random_device &rd, uniform_real_distribution<float> &dis) {
    Point p = Point(dim);
    for (int i = 0; i < dim; ++i) {
        p[i] = dis(rd); 
    }
    return p;
}

PointVector generate_point_vector(const uint &size, const uint &dim, random_device &rd, uniform_real_distribution<float> &dis) {
    PointVector v = PointVector (size);
    for (int i = 0; i < size; ++i) {
        v[i] = generate_point(dim, rd, dis);
    }
    return v;
}

void print_results(function<void(const Point)> f) {

}

int main() {
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<float> dis(-MAX_NUM_VAL, MAX_NUM_VAL);
    PointVector v = generate_point_vector(SIZE, DIMENSIONS, rd, dis);

    INIT_TIME();
    cout << "RKDTree ";
    TIME(RKDTree rkd = RKDTree(MAX_SEARCH_LIM, 10, NUM_HIGH_VAR, v));
    cout << "KDTree ";
    TIME(KDTree kd = KDTree(DIMENSIONS, &rkd.data));
    
    Point p = generate_point(DIMENSIONS, rd, dis);

    cout << "====== KDTree search ======" << endl;
    TIME(Point p_found_kd = kd.search(p));
    cout << "Point: " << p_found_kd << endl;
    double kd_dist = KDTree::distance(p_found_kd, p);
    cout << "Distance: " << kd_dist << endl;

    cout << "====== RKDTree search ======" << endl;
    TIME(Point p_found_rkd = rkd.search(p));
    cout << "Point: " << p_found_rkd << endl;
    double rkd_dist = KDTree::distance(p_found_rkd, p);
    cout << "Distance: " << rkd_dist << endl;

    cout << "========== Results ==========" << endl;
    cout << "Distance difference: " << rkd_dist - kd_dist << endl;
}