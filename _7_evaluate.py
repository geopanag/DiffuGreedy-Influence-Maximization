# -*- coding: utf-8 -*-
"""
@author: georg

Evaluate the selected seeds using the test cascades
"""

import os
import pandas as pd
from igraph import *
import time
import numpy as np
import operator
import glob


def evaluate_distinct(seed_set_cascades):
    """
    Measure the number of distinct nodes in the test cascades started from the seed set
    """
    combined = set()    
    for i in seed_set_cascades.keys():
        for j in seed_set_cascades[i]:    
            combined = combined.union(j)
    return len(combined)
        
        
"""        
Main
"""
os.chdir("path\\to\\Data")

#------- To map the simpath seeds with the original ids
g_bern = Graph.Read_Ncol("follower_bern.txt")
g_time = Graph.Read_Ncol("follower_time.txt")
g_fused = Graph.Read_Ncol("follower_fused.txt")
 
#------- Use it to tally the ids from netrate seeds to the real names
top = pd.read_csv("top_nodes.csv")

log= open("Logs\\time_log_evaluate.txt","a")
#-------- Read all the seed sets
for seed_set_file in glob.glob("Seeds\\"):
    
    print(seed_set_file)
    f = open(seed_set_file,"r")
    l = f.next().replace("\n","")
    
    #-------- Map the node numbers in the sets to the real node ids
    if("centr_" in seed_set_file or "diffusion_" in seed_set_file or "follower_weighted" in seed_set_file):
        seed_set_all = [x for x in l.split(" ") if x!='']
    if "netrate_" in seed_set_file:
		top_c = list(top["Degree"].values)
		top_dict ={v:b for v,b in enumerate(top_c)} 
        seed_set_all = [top_dict[int(x)] for x in l.split(" ") if x!='']
    else: #----  Simpath seeds correspond to  node ids of databased networks
		if "follower_bern" in seed_set_file:
			g = Graph.Read_Ncol("follower_bern.txt")
		elif "follower_time" in seed_set_file:
			g = Graph.Read_Ncol("follower_time.txt")
		elif "follower_fused" in seed_set_file:
			g = Graph.Read_Ncol("follower_fused.txt")
		seed_set_all = [g.vs[int(x)]["name"] for x in l.split(" ") if x!='']
    f.close()
    
    #------- Estimate the spread of that seed set in the test cascades
    spreading_of_set = {}
    for seed_set_size in range(10,110,10):
        spreading_of_set[seed_set_size] = 0
        
        seeds = seed_set_all[0:seed_set_size]
        start = time.time()
         
        #------- List of cascades for each seed
        seed_cascades =  {}
        for s in seeds:
            seed_cascades[str(s)] = []
       
        #------- Fill the seed_cascades
        seed_set = set()
        with open("test_cascades.txt") as f:
            for line in f:
                cascade = line.split(";")
                op_id = cascade[1].split(" ")[0]
                cascade = set(map(lambda x: x.split(" ")[0],cascade[2:]))
                if op_id in seed_cascades:
                    seed_cascades[op_id].append(cascade)
                    seed_set.add(op_id)
           
        seed_set_cascades = { seed: seed_cascades[seed] for seed in seed_set if len(seed_cascades[seed])>0 }
        print("Seeds found :",len(seed_set_cascades))
    
        spreading_of_set[seed_set_size] = evaluate_distinct(seed_set_cascades)
                
    pd.DataFrame({"Feature":spreading_of_set.keys(), "Cascade Size":spreading_of_set.values()}).to_csv(seed_set_file.replace("Seeds\\","Results\\spreading_"),index=False)
    
    log.write("Time to estimate spreading for :"+seed_set_file+" :"+str(time.time() - start)+"\n")
    
log.close()
