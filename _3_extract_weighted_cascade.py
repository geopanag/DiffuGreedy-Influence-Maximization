# -*- coding: utf-8 -*-
"""
@author: georg

Add edge weights to the follower networks based on the number of possible influencers of the end node (weighted cascade)
"""
import os
from igraph import *
import time

"""
Main
"""
os.chdir("path\\to\\Data")

log= open("Logs\\time_log.txt","a")

g = Graph.Read_Pickle("trained_network.pickle")

#--------------------------
weighted_graph = open("follower_weighted.txt","w")
    
start = time.time()
for v in range(0,len(g.vs)):
    
    #----- The out-edges signify who v follows, so who can influence it
    edges = g.incident(v, mode="out") 
    if(len(edges)==0):
        continue

    #------  Store the influence edges of V  in format v1 -influences- v2
    v2 = str(g.vs[v]["name"])
    v1s = map(lambda x: str(x.tuple[0]),g.es[edges])
    edge_weight = str("%.6f" % (float(1)/len(edges)))
     
    weighted_graph.write("".join([str(g.vs[v1]["name"]+" "+v2+" "+edge_weight+"\n") for v1 in v1s]))
    
    if(v%1000==0):
        print("-------------------",v)
        
weighted_graph.close()

attribute = open("follower_weighted_attribute.txt","w")
attribute.write("n="+str(len(g.vs)+1)+"\n")
attribute.write("m="+str(len(g.es))+"\n")
attribute.close()

log.write("Time to extract weighted cascade follower network:"+str(time.time()-start)+"\n")
log.close()
