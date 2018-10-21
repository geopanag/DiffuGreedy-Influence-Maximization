# -*- coding: utf-8 -*-
"""
@author: georg

Store the inferred network from netrate into an edgelist, using weights based on 
the same methodology as in simpath paper
Compare the neighborhoods of each node in the inferred network with the actual follower network
"""

import os
from igraph import *
import pandas as pd
import numpy as np
import random as rand
import networkx as nx
from PMIA import PMIA


def create_netrate_network(fname):
    """
    #Create the netrate inferred netwrok from the adjecency matrix
	"""
    netrate_net = Graph(directed=True)
    netrate_net.add_vertices(3000)
    
    netrate_file = open(fname,"r")
    
    #------ Loop through all rows of the adjecency and add the edges
    node_i = 0    
    inferred_edges = []
    for line in netrate_file:
        #---------- All edge weights are almost 0
        for node_j, weight in enumerate(line.replace("\n","").split(",")): 
            if weight!='0':
                inferred_edges.append((node_i,node_j))
        node_i+=1
       
    netrate_net.add_edges(inferred_edges)
        
    return netrate_net


def store_edgelist(netrate_net,col,fname):
    """  
    #All weights given by netrate are practically zero, so derive the weights with different methods
    """
    
    #----- Store the edgelist with weights as defined for weighted cascade in kempe 2003 paper
    for v in netrate_net.vs:
        edges = netrate_net.incident(v, mode="in")
        for e in edges:
                netrate_net.es[e]["weight"] = float(1)/len(edges)
                
    edge_list =  open(fname,"w")
    for edge in netrate_net.es:
        edge_list.write(str(edge.tuple[0])+" "+str(edge.tuple[1])+" "+str(edge["weight"])+"\n")    
    edge_list.close()

    
    
    
"""
Main
"""
os.chdir("path\\to\\Data")

#------- Compare the neighborhoods of each node in the follower and inferred network
follow_network = Graph.Read_Ncol("active_network.txt")

#----- To tally the ids in netrate graph with the ids in the follower graph  for the comparison
top = pd.read_csv("top_nodes.csv")

col  = "Degree"
top_c = list(top[col].values)
id_name ={v:b for v,b in enumerate(top_c)} 
    
if col == "Total_cascades":
    col = "no_cascades"
    
col = col.lower()
    
#---- Retrieve the netrate network stored at netrate/
netrate_net = create_netrate_network("netrate\\netrate_net_"+col+".txt")
    
#---- Store it with appropriate weighting methodology to use it with Simpath
fname = "netrate\\netrate_"+col.lower()+"_deg.txt"
store_edgelist(netrate_net,col,fname)
    
#----- Compute average precision of the infered neighbors and the real ones
avg_prec = 0
for i,node in enumerate(netrate_net.vs):        
    inferred_neighs =  netrate_net.neighbors(node)
    if len(inferred_neighs)==0:
    	continue
        
    #---- Find how many of the inferred neighbors are indeed followers
    real_neighs = follow_network.neighbors(follow_network.vs.find(str(id_name[i])))
    prec = 0
    for n in inferred_neighs:        
    	if id_name[n] in real_neighs:
	    prec+=1
    avg_prec += float(prec)/len(inferred_neighs)

print(col+" average precision:"+str(avg_prec*100/i))

#----- Run PMIA
g = nx.read_edgelist(fname, nodetype=int, data=(('weight',float),),create_using=nx.DiGraph())
start = time.time()           
theta = 1.0/320
Ep = dict()
with open(fname) as f:
    for line in f:
	parts = line.split()
	Ep[(int(parts[0]), int(parts[1]))] = float(parts[2])

S = PMIA(g, 100, theta, Ep)
log.write("PMIA for "+fname+" :"+str(time.time()-start)+"\n")
        
f = open("Seeds/"+fname.replace(".txt","_pmia.txt"),"w")
for i in S:
    f.write(str(i)+" ")
f.close()    

     
