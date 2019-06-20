#include "vptree.hpp"
#include <iostream>
#include <fstream>
#include <chrono>

using namespace std;

#define SIZE 100000
#define DIMENSIONS 3
#define MAX_NUM_VAL 100
#define N_NEIGHBORS 10000
#define ITERATIONS 100

#define INIT_TIME()                                     \
chrono::time_point<chrono::system_clock> start, end;    \
double elapsed_time;                                    \


#define TIME(code)                                                              \
start = chrono::system_clock::now();                                            \
code;                                                                           \
end = chrono::system_clock::now();                                              \
elapsed_time = chrono::duration_cast<chrono::microseconds> (end-start).count(); \

typedef vector<double> Point;
typedef vector<Point> PointVector;

ostream & operator << (std::ostream & out, const Point & p) {
    out << "[";
    if (!p.empty()) {
        out << p[0];
        for (int j = 1; j < p.size(); ++j)
            out << "," << p[j];
    }
    out << "]";
    return out;
}

ostream & operator << (std::ostream & out, const PointVector & v) {
    out << "[";
    if (!v.empty()) {
        out << v[0];
        for (int j = 1; j < v.size(); ++j)
            out << "," << v[j];
    }
    out << "]";
    return out;
}

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

int main() {
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<float> dis(-MAX_NUM_VAL, MAX_NUM_VAL);
    PointVector v = generate_point_vector(SIZE, DIMENSIONS, rd, dis);

    INIT_TIME();
    ofstream data, queries, results, times;
    times.open("times.txt");
    TIME(vpt::VpTree vptree = vpt::VpTree(v));
    times << "[" << elapsed_time;


    data.open ("data.txt");
    data << v << endl;
    data.close();
    queries.open ("queries.txt");
    results.open ("results.txt");

    for (int i = 0; i < ITERATIONS; ++i) {
        Point p = generate_point(DIMENSIONS, rd, dis);
        queries << p << endl;

        TIME(vpt::DistancesIndices d = vptree.getNearestNeighbors(p, N_NEIGHBORS));
        times << ", " << elapsed_time;
        results << "[";
        if (!d.second.empty())
            results << "(" << d.first[0] << ", " << v[d.second[0]] << ")";
        for (int j = 1; j < d.second.size(); ++j) {
            results << ", (" << d.first[j] << ", " << v[d.second[j]] << ")";
        }
        results << "]" << endl;
    }
    times << "]";
    times.close();
    results.close();
    queries.close();

}