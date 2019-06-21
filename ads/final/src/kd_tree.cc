#include "kd_tree.h"

ostream & operator << (std::ostream & out, const KDTree & kdt) {
    if (kdt.data != NULL) {
        out << "( " << kdt.axis << " | " << kdt.data->v[kdt.location].point[0];
        for (int i = 1; i < kdt.data->v[kdt.location].point.size(); ++i) {
            out << "," << kdt.data->v[kdt.location].point[i];
        }
        out << " )";
        out << kdt.left << kdt.right;
    }
    else
        out << "*";
    return out;
}

ostream & operator << (std::ostream & out, const KDTree* kdt) {
    if (kdt != NULL and kdt->data != NULL) {
        out << endl << "( " << kdt->axis ;
        out << " | " << kdt->data->v[kdt->location].point[0];
        for (int i = 1; i < kdt->data->v[kdt->location].point.size(); ++i) {
            out << "," << kdt->data->v[kdt->location].point[i];
        }
        out << " )";
        out << kdt->left << kdt->right;
    }
    else
        out << "*";
    return out;
}

KDTree::KDTree () {
    this->dim = 0;
    this->axis = 0;
    this->location = 0;
    this->left = NULL;
    this->right = NULL;
    this->data = NULL;
}

KDTree::KDTree (const uint &dim) {
    this->dim = dim;
}

KDTree::KDTree (const uint &dim, Data* data) {
    this->dim = dim;
    this->data = data;
    if (this->check_dimension(this->data->v)) {
        this->build_standard(dim, data, this->data->v);
    }
    else
        throw string("Dimensions does not match.");
}

bool KDTree::check_dimension(const IPointVector &v) {
    for (auto element : v) {
        if (element.point.size() != this->dim)
            return false;
    }
    return true;
}

IPoint KDTree::qselect (const uint &k, const uint &axis, const IPointVector &v) {
    int idx = rand() % v.size();
    IPoint pivot = v[idx];
    IPointVector left, right;
    uint elements_like_pivot = 0;
    for (IPoint element: v) {
        if (element.point[axis] < pivot.point[axis])
            left.push_back(element);
        else if (element.point[axis] > pivot.point[axis])
            right.push_back(element);
        else
            ++elements_like_pivot;
    }
    if (k < left.size())
        return qselect(k, axis, left);
    else if (k >= left.size() + elements_like_pivot)
        return qselect(k-left.size()-elements_like_pivot, axis, right);
    else
        return pivot;
}

//Point KDTree::median(const uint &axis, IPointVector v) {
//    uint median_pos;
//    if (v.size() % 2 == 0) 
//        median_pos = v.size()/2;
//    else
//        median_pos = (v.size()-1)/2;
//    auto comp = [&](Point x, Point y) {return x[axis] < y[axis];};
//    sort(v.begin(), v.end(), comp);
//    print_point_vector(v);
//    return v[median_pos];
//}

IPoint KDTree::median (const uint &axis, const IPointVector &v) {
    uint median_pos;
    if (v.size() % 2 == 0) 
        median_pos = v.size()/2;
    else
        median_pos = (v.size()-1)/2;
    return KDTree::qselect(median_pos, axis, v);
}

void KDTree::build_standard (const uint &dim, Data* data, const IPointVector &v) {
    if (!v.empty()) {
        this->dim = uint(dim);
        this->data = data;
        this->axis = this->data->hv_idx[rand() % this->data->hv_idx.size()];
        this->location = KDTree::median(this->axis,v).idx;
        IPointVector left, right;
        for (IPoint element: v) {
            if (element.point != this->current_point()) {
                if (element.point[this->axis] <= this->current_point()[this->axis])
                    left.push_back(element);
                else
                    right.push_back(element);
            }
        }
        if (!left.empty()) {
            this->left = new KDTree(this->dim);
            this->left->build_standard(dim, data, left);
        }
        else
            this->left = NULL;

        if (!right.empty()) {
            this->right = new KDTree(this->dim);
            this->right->build_standard(dim, data, right);
        }
        else
            this->right = NULL;
    }
    else {
        this->axis = 0;
        this->location = 0;
        this->left = NULL;
        this->right = NULL;
        this->data = NULL;
    }
}

float KDTree::distance(const Point &p, const Point &q) {
    float sum = 0;
    for (int i = 0; i < p.size(); ++i) {
        sum += pow(q[i] - p[i], 2);
    }
    return sum;
}

void KDTree::explore_children(float &best_distance, Point &best_p, const Point &current_p, int &n, const Point &p) {
    uint left_or_right = rand() % 2;
    bool check_other = true;
    if (left_or_right == 0) {
        // if (this->left != NULL) {
        //     this->left->recursive_search(best_distance, best_p, n, p);
        //     Point splitting_coordinate = p;
        //     splitting_coordinate[this->axis] = current_p[this->axis];
        //     check_other = distance(p, splitting_coordinate) < best_distance;
        // }
        // if (check_other && n != 0 && this->right != NULL)
        //     this->right->recursive_search(best_distance, best_p, n, p);
        if (n != 0 and this->left != NULL and p[this->axis] - best_distance <= current_p[this->axis])
            this->left->recursive_search(best_distance, best_p, n, p);
        if (n != 0 and this->right != NULL and p[this->axis] + best_distance > current_p[this->axis])
            this->right->recursive_search(best_distance, best_p, n, p);
    }
    else {
        // if (this->right != NULL) {
        //     this->right->recursive_search(best_distance, best_p, n, p);
        //     Point splitting_coordinate = p;
        //     splitting_coordinate[this->axis] = current_p[this->axis];
        //     check_other = distance(p, splitting_coordinate) < best_distance;
        // }
        // if (check_other && n != 0 && this->left != NULL)
        //     this->left->recursive_search(best_distance, best_p, n, p);
        if (n != 0 and this->right != NULL and p[this->axis] + best_distance > current_p[this->axis])
            this->right->recursive_search(best_distance, best_p, n, p);
        if (n != 0 and this->left != NULL and p[this->axis] - best_distance <= current_p[this->axis])
            this->left->recursive_search(best_distance, best_p, n, p);
        
    }
}

void KDTree::recursive_search(float &best_distance, Point &best_p, int &n, const Point &p) {
    Point current_p = this->current_point();
    float d = distance(p, current_p);
    if (d < best_distance) {
        best_distance = d;
        best_p = current_p;
    }
    --n;
    if (n != 0)
        explore_children(best_distance, best_p, current_p, n, p);
}

Point KDTree::limited_search(int &n, const Point &p) {
    if (this->dim == p.size()) {
        Point current_p = this->current_point();
        Point best_p = current_p;
        float best_distance = distance(p, best_p);
        explore_children(best_distance, best_p, current_p, n, p);
        return best_p;
    }
    else {
        throw string("Searched point has different dimension.");
        return Point (0);
    }
    return p;
}

Point KDTree::search(const Point &p) {
    if (this->dim == p.size()) {
        Point current_p = this->current_point();
        Point best_p = current_p;
        float best_distance = distance(p, best_p);
        int n = -1;
        explore_children(best_distance, best_p, current_p, n, p);
        cout << "Visited nodes:" << -n << endl;
        return best_p;
    }
    else {
        throw string("Searched point has different dimension.");
        return Point (0);
    }
}

Point KDTree::current_point() {
    if (this->data == NULL)
        return Point ();
    return this->data->v[this->location].point;
}

// int main() {
//     srand (time(NULL));
//     try {
//         Data* data = new Data;
//         PointVector v = {{5,2},{9,5},{2,6},{4,3},{3,4},{6,1}};
//         data->v = pointvector_to_ipointvector(v);
//         data->hv_idx = {};
//         KDTree t (2, data);
//         cout << t << endl;
//         Point p = t.search({9,4});
//         int n = 2;
//         Point q = t.limited_search(n,{9,4});
//         cout << p <<  endl;
//         cout << q <<  endl;
//     }
//     catch (string s) {
//         cout <<s << endl;
//     }
// }