#include "tree.h"

int main () {
    vector<int> v = {1,2,3,4,5,6,7};
    Tree<int>* t = new Tree<int> (v);
    try {
        cout << t->left()->left()->value() << endl;
    }
    catch (string s) {
        cout << s << endl;
    }
}