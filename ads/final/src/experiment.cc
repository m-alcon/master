#include <random>
#include "rkd_tree.h"

#define MAX_NUM_VAL 10000
#define MAX_SEARCH_LIM 1000
#define NUM_HIGH_VAR 32
#define SIZE 100000
#define DIMENSIONS 128



PointVector generate_point_vector(const uint &size, const uint &dim) {
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<float> dis(-MAX_NUM_VAL, MAX_NUM_VAL);
    PointVector v = PointVector (size);
    for (int i = 0; i < size; ++i) {
        v[i] = Point(dim);
        for (int j = 0; j < dim; ++j) {
            v[i][j] = dis(rd); 
        }
    }
    return v;
}

int main() {
    PointVector v = generate_point_vector(SIZE, DIMENSIONS);
    RKDTree rkd = RKDTree(MAX_SEARCH_LIM, 10, NUM_HIGH_VAR, v);
}