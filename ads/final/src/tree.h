#include <iostream>
#include <string>
#include <vector>

using namespace std;

template <class T>
class Tree {
    public:
        Tree<T> ();
        Tree<T> (const T &data) {
            this->data = data;
            this->l_child = NULL;
            this->r_child = NULL;
        }

        Tree<T> (const vector<T> &v) {
            if (v.size() > 0) {
                this->data = v[0];
                this->l_child = Tree::create_tree(1,v);
                this->r_child = Tree::create_tree(2,v);
            }
        }

        T value() {
            return this->data;
        }

        bool has_left() {
            if (this->l_child != NULL)
                return true;
            return false;
        }

        bool has_right() {
            if (this->r_child != NULL)
                return true;
            return false;
        }

        Tree<T>* left() {
            if (this->has_left())
                return this->l_child;
            throw string("Accessing empty left child.");
        }


        Tree<T>* right() {
            if (this->has_right())
                return this->r_child;
            throw string("Accessing empty right child.");
        }
        

    private:
        T data;
        Tree<T> *l_child;
        Tree<T> *r_child;

        static Tree<T>* create_tree(int i, const vector<T> &v) {
            if (i < v.size()) {
                Tree<T>* root = new Tree<T> (v[i]);
                root->l_child = Tree::create_tree(2*i+1, v);
                root->r_child = Tree::create_tree(2*i+2, v);
                return root;
            }
            return NULL;
        }
};