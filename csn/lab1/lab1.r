library(igraph)
setwd("/home/malcon/Master/Git/csn/lab1") # setting my working directory

# BASICS

## Creating graphs
g <- graph( c(1,2, 1,3, 2,3, 3,5), n=5 )
V(g)
E(g)
g <- graph.empty() + vertices(letters[1:10], color="red")
g <- g + vertices(letters[11:20], color="blue")
g <- g + edges(sample(V(g), 30, replace=TRUE), color="green")
V(g)
E(g)

### Loading graphs
g <- read.graph("graph.txt", format="edgelist")
V(g)
E(g)
IG <- induced.subgraph(g,2:4)
V(IG)
g=set_vertex_attr(g,"name",value = 0:3)
karate <- read.graph("http://cneurocvs.rmki.kfki.hu/igraph/karate.net", format="pajek")
V(karate)
E(karate)

### Graph generators
er_graph <- erdos.renyi.game(100, 2/100)
ws_graph <- watts.strogatz.game(1, 100, 4, 0.05)
ba_graph <- barabasi.game(100)

## Manipulating attributes in graphs
