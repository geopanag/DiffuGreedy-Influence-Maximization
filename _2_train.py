# -*- coding: utf-8 -*-
"""
@author: georg

Extract summary features about the participation of nodes in the cascades
Extract node centralities from the follower network and the cascades
Add edge weights to the follower network that correspond to the influence 
as measured in th cascades (copying frequency and time difference)
"""

import os
from igraph import *
import time
import pandas as pd
from datetime import datetime


def remove_duplicates(cascade_nodes,cascade_times):
    """
    # Some tweets have more then one retweets from the same person
    # Keep only the first retweet of that person
    """
    duplicates = set([x for x in cascade_nodes if cascade_nodes.count(x)>1])
    for d in duplicates:
        to_remove = [v for v,b in enumerate(cascade_nodes) if b==d][1:]
        cascade_nodes= [b for v,b in enumerate(cascade_nodes) if v not in to_remove]
        cascade_times= [b for v,b in enumerate(cascade_times) if v not in to_remove]

    return cascade_nodes, cascade_times


def train_graph(g,train_file):
    """
    # Use the cascades to update the edge attributes and the node features
    """
    f = open(train_file)
    g.es["Inf"] = 0
    g.es["Dt"] = 0
	
    #----- Iterate through training cascades
    idx = 0
    deleted_nodes = []
    for line in f:
        
        parts = line.replace("\n","").split(";")
        day = int(parts[0])
        cascade_size = len(parts)-1
        
        cascade_nodes = map(lambda x:  x.split(" ")[0],parts[1:])
        cascade_times = map(lambda x:  datetime.strptime(x.split(" ")[1], '%Y-%m-%d-%H:%M:%S'),parts[1:])
        
        #---- Remove retweets by the same person in one cascade
        cascade_nodes, cascade_times = remove_duplicates(cascade_nodes,cascade_times)
        
        for i in range(len(cascade_nodes)):
            if(i==(len(cascade_nodes)-1) ):
                break
            
            #--- Add to the cascade graph all i's edges that point to j and abide to the time constraint
            for j in range(i+1,len(cascade_nodes)):
                try:
                    if(g.es[edge]["weight"]<=day): #and g.es[edge]["Type"]=="Follow"):
                        #------ i influences j
                        cascade_subgraph.add_edge(cascade_nodes[i], cascade_nodes[j])
                        #------ add to the graph edges attributes
                        g.es[edge]["Inf"]+=1
                        g.es[edge]["Dt"]+= (cascade_times[j]-cascade_times[i]).total_seconds()
                except:
                    pass
		idx+=1
        if(idx%100==0):
            print("-------------------",idx)
        
    #-----80 deleted nodes
    print("Number of nodes not found in the graph: ",len(deleted_nodes))
    f.close()
    return g



"""
Main
"""

os.chdir("path\\to\\Data")


log= open("Logs\\time_log.txt","a")

g = Graph.Read_Ncol("active_network.txt")

start = time.time()
g = train_graph(g,"train_cascades.txt")
log.write("Training time:"+str(time.time()-start)+"\n")


#----------- Subset the graph up to day 25 and remove the weight (which is the day)
log.write("Number of edges with the last week:"+str(len(g.es))+"\n")
for i in range(26,33): 
    g.delete_edges(g.es.select(weight=i))
del g.es["weight"]
log.write("Number of edges without last week:"+str(len(g.es))+"\n")  #-- 9 mil difference

#------------ Store the network
g.write_pickle("trained_network.pickle")

#------------ Compute structural node statistics
start = time.time()
kcores = g.shell_index(mode="IN")
log.write("K-core time:"+str(time.time()-start)+"\n")


#------------ Store the node features
pd.DataFrame({"Nodes":g.vs["name"],
			  "Degree":g.indegree(),
              "Kcores":kcores}).to_csv("centralities.csv",index=False)

