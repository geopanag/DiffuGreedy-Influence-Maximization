# -*- coding: utf-8 -*-
"""
@author: georg

Create 3 versions of the follower network, with edge weights based on the strength of influence,
the time delay of influence, and their product. 
"""


import os
from igraph import *
import time
import numpy as np


"""
Main
"""
os.chdir("path\\to\\Data")
log= open("Logs\\time_log.txt","a")

g = Graph.Read_Pickle("trained_network.pickle")

time_graph = open("follower_databased_time.txt","w")
bernouli_graph = open("follower_databased_bern.txt","w")
   
#-------- Parameter to scale DTs
delta =1000

start = time.time()
for i,v in enumerate(g.vs):
    
    total_cascades = v["Cascades_participated"]+v["Cascades_started"]
    #---- Total cascades being zero means the node only exists in the test set
    if(total_cascades!=0): 
	#------ V can influence the nodes that follow it
        edges = g.incident(v, mode="in")
	
        for edge in g.es[edges]:            
            #------- Number of times influenced / number of times the influencer did an action
            bernouli_weight = str("%.6f" % (float(edge["Inf"])/total_cascades))
            if float(bernouli_weight)>0.000001:
                bernouli_graph.write(str(g.vs[edge.tuple[1]]["name"])+" "+str(g.vs[edge.tuple[0]]["name"])+" "+bernouli_weight+"\n")    
            #------- Avg Dt / delta
            if edge["Dt"]>0:
                time_weight = str("%.6f" % (np.exp(-(float(edge["Dt"])/edge["Inf"])/delta)))
                time_graph.write(str(g.vs[edge.tuple[1]]["name"])+" "+str(g.vs[edge.tuple[0]]["name"])+" "+time_weight+"\n")
                
    if i%1000==0:
        print("-------------------",v)
		
time_graph.close()
bernouli_graph.close()

log.write("Time to extract time and bernouli graphs:"+str(time.time()-start)+"\n")
log.close()

#--- Create a fused version with weight = bern*time
f = open("follower_fused.txt","w")
g1 = Graph.Read_Ncol("follower_time.txt")
g2 = Graph.Read_Ncol("follower_bern.txt")

for e1 in g1.es:
    try:
        e2 = g2.es[g2.get_eid(e1.tuple[0],e1.tuple[1])]
		#--------- Keep the original names
        f.write(str(g1.vs[e1.tuple[0]]["name"])+" "+str(g1.vs[e1.tuple[1]]["name"])+" "+str(e2["weight"]*e1["weight"])+"\n")
    except:
        continue
f.close()

#--- Prepare files for SIMPATH
#--- The graphs have to have ids in [0,n-1]
for c in ["fused","time","bern"]:
	g = Graph.Read_Ncol("follower_"+c+".txt")
	f = open("follower_"+c+"_simpath.inf","w")
	f.write("# first line")
	for e in g.es:
		w = str("%.6f" % (e["weight"]))
		f.write(str(e.tuple[0])+" "+str(e.tuple[1])+" "+w+"\n")
	f.close()
		
		
