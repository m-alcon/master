#include <ilcplex/ilocplex.h>
#include <math.h> 
#include <vector>
#include <fstream>
ILOSTLBEGIN

#define MAX_DEPTH 5

bool is_bit_up(const unsigned int &bit_pos, const int &number) const {
  return ((unsigned int) pow(2, bit_pos) & number) != 0;
}

vector<int> read_input() {
  int n;
  cin >> n;
  vector<int> truth_table(pow(2,n));
  for (int i = 0; i < pow(2,n); ++i)
    cin >> truth_table[i];
  return truth_table;
}

IloNumVar var(const int &h, const int &w, IloNumVarArray &V)  {
  if (w >= pow(2,h))
    cerr << "ERR: Trying to access an invalid node." << endl;
  return V[(pow(2,h)-1)+w];
}

void circuit_constraints(const int &h, const int &w, const int &depth, const int &truth_idx, 
                          IloNumVarArray &Z, IloNumVarArray &I, IloNumVarArray &N, IloModel &model) {
  if (h == depth) {
    model.add( var(h, w, N) == 0 );
  }
  else {
    constraint_creation(h+1,   2*w, depth, truth_idx, Z, I, N, model);
    constraint_creation(h+1, 2*w+1, depth, truth_idx, Z, I, N, model);
  }

}


int main () {

  IloEnv env;
  IloModel model(env);

  const vector<int> truth_table = read_input();
  const int n = log2(truth_table.size())
  const int circuit_size = pow(2,depth+1)-1;

  for (int depth = 0; depth < MAX_DEPTH; ++i) {
    IloNumVarArray zero_nodes   = IloNumVarArray(env, circuit_size, 0, 1, ILOINT);
    IloNumVarArray input_nodes  = IloNumVarArray(env, circuit_size, 0, 1, ILOINT);
    IloNumVarArray nor_nodes    = IloNumVarArray(env, circuit_size, 0, 1, ILOINT);

    // Each node must be only of one type
    for (int i = 0; i < circuit_size; ++i) {
      model.add( zero_nodes[i] + input_nodes[i] + nor_nodes[i] == 1 )
    }
    
  }

  
  S = IloNumVarArray(env, N_Types * N_Periods, 0, IloInfinity, ILOINT);
  X = IloNumVarArray(env, N_Types * N_Periods, 0, IloInfinity, ILOFLOAT);

  // for (int t = 0; t < N_Types; ++t)
  //   for (int p = 0; p < N_Periods; ++p)
  //     model.add( n(t, p) <= avail_unit[t] );

  // for (int p = 0; p < N_Periods; ++p) {
  //   IloExpr expr(env);
  //   for (int t = 0; t < N_Types; ++t)
  //     expr += x(t, p);

  //   model.add( expr >= dem[p]);
  //   expr.end();
  // }

  // IloExpr obj(env);

  // for (int t = 0; t < N_Types; ++t)
  //   for (int p = 0; p < N_Periods; ++p) {
  //     obj +=
  //       cost_min[t] * len[p] *  n(t, p) +
  //       cost_x_h[t] * len[p] * (x(t, p) - min_output[t] * n(t, p)) +
  //       cost_ini[t] * s(t, p);
  //   }
  // model.add(IloMinimize(env, obj));
  // obj.end();

  IloCplex cplex(model);
  cplex.solve();
  cout << cplex.getObjValue() << endl;
  env.end();
}
