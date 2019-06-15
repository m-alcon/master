#include <iostream>
#include <string>
#include <algorithm>
#include <vector>
#include <numeric>
#include <math.h>   
#include <chrono>
using namespace std;

#define INIT_TIME()                                     \
chrono::time_point<chrono::system_clock> start, end;    \
double elapsed_time;                                    \


#define TIME(code)                                                              \
start = chrono::system_clock::now();                                            \
code;                                                                           \
end = chrono::system_clock::now();                                              \
elapsed_time = chrono::duration_cast<chrono::milliseconds> (end-start).count(); \
cout << "Time: " << elapsed_time/1000 << endl;                                       \

typedef vector<float> Point;

struct IPoint {
    Point point;
    uint idx;
};

typedef vector<Point> PointVector;
typedef vector<IPoint> IPointVector;

struct Data {
    IPointVector v;
    vector<uint> hv_idx; //High variance indexes
};

ostream & operator << (std::ostream & out, const Point & p);
ostream & operator << (std::ostream & out, const IPoint & p);
ostream & operator << (std::ostream & out, const IPointVector & v);
ostream & operator << (std::ostream & out, const PointVector & v);
IPointVector pointvector_to_ipointvector(const PointVector v);
vector<float> variance(const IPointVector &v);
vector<uint> compute_high_variance_idx(const uint &k, IPointVector v);