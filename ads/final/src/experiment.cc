#include <random>
#include "rkd_tree.h"

#define MAX_NUM_VAL 10
#define MAX_SEARCH_LIM 60000
#define NUM_HIGH_VAR 16
#define SIZE 100000
#define DIMENSIONS 128
#define TREES 16
#define ITERATIONS 1000

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
    cout << "========= Construction =========" << endl;
    cout << "RKDTree: " << endl;
    TIME(RKDTree rkd = RKDTree(MAX_SEARCH_LIM, TREES, NUM_HIGH_VAR, v));
    cout << "KDTree: " << endl;
    TIME(KDTree kd = KDTree(DIMENSIONS, &rkd.data));

    cout << "========== Execution ==========" << endl;
    // for (int search_lim = 1000; search_lim <= SIZE; search_lim += 1000) {
    //     rkd.n = search_lim;
    //     int count_correct = 0;
    //     for (int i = 0; i < ITERATIONS; ++i) {
    //         Point p = generate_point(DIMENSIONS, rd, dis);
    //         cout << "RKDTree: " << endl;
    //         TIME(Point p_found_rkd = rkd.search(p));
    //         double rkd_dist = KDTree::distance(p_found_rkd, p);
    //         cout << "   Distance: " << rkd_dist << endl;

    //         cout << "KDTree: " << endl;
    //         TIME(Point p_found_kd = kd.search(p));
    //         double kd_dist = KDTree::distance(p_found_kd, p);
    //         cout << "   Distance: " << kd_dist << endl;

    //         cout << "Difference: " << rkd_dist - kd_dist << endl;
    //         if (rkd_dist - kd_dist == 0) ++count_correct;
    //         cout << "--------------------------------" << endl;
    //     }
    //     cout << "* " << search_lim << " " << count_correct << endl; 
    //}
    int count_correct = 0;
    for (int i = 0; i < ITERATIONS; ++i) {
        Point p = generate_point(DIMENSIONS, rd, dis);
        cout << "RKDTree: " << endl;
        TIME(Point p_found_rkd = rkd.search(p));
        double rkd_dist = KDTree::distance(p_found_rkd, p);
        cout << "   Distance: " << rkd_dist << endl;

        cout << "KDTree: " << endl;
        TIME(Point p_found_kd = kd.search(p));
        double kd_dist = KDTree::distance(p_found_kd, p);
        cout << "   Distance: " << kd_dist << endl;

        cout << "Difference: " << rkd_dist - kd_dist << endl;
        if (rkd_dist - kd_dist == 0) ++count_correct;
        cout << "--------------------------------" << endl;
    }
    cout << "* " << count_correct << endl;
}
