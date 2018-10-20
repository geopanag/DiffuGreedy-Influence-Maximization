# -*- coding: utf-8 -*-
"""
@author: georg

Influence Maximization using the train cascades
"""

import os
from igraph import *
import numpy as np
import time

def DiffusionCELF (node_cascades, k=100):
    Q = [] 
    S = []
    final_cascade = set()
    
    nid = 0
    msg = 1
    cas = 2
    iteration = 3 
    
    for u in node_cascades.keys():
        temp_l = []
        temp_l.append(u) #u
        #------
        cascades = node_cascades[u]
        index, value = max(enumerate([len(final_cascade.union(set(casc))) for casc in cascades]), key=operator.itemgetter(1))
        temp_l.append(value) # msg
        temp_l.append(index) # which cascade of  u gives the best
        temp_l.append(0) #iteration
        Q.append(temp_l)
      
    Q = sorted (Q, key=lambda x:x[1],reverse=True)
        
    #----- Celf
    while len(S) < k :
        u = Q[0]
        if (u[iteration] == len(S)):
            if(len(S)%20==0):
                print(len(S))
            #----- Store the new seed
            S.append(u[nid])
            final_cascade = final_cascade.union(node_cascades[u[nid]][u[cas]])
            #----- Delete Q
            Q = [l for l in Q if l[0] != u[nid]]
        
        else:
            #----- Update this node
            cascades = node_cascades[u[nid]]
            index, value = max(enumerate([len(final_cascade.union(set(casc))) for casc in cascades]), key=operator.itemgetter(1))
            u[msg] = value
            u[cas] = index
            u[iteration] = len(S)
            Q = sorted(Q, key=lambda x:x[1],reverse=True)
        
    return S, len(final_cascade)



def DiffusionGreedy(seed_set_cascades,seed_set_size=100):
    seed_set = []
    final_cascade = set()
    while len(seed_set)<seed_set_size:
        max_seed = ""
        max_val = 0
        max_idx = np.NaN
        
        for seed, cascades in seed_set_cascades.iteritems():
            #----- The marginal gain is given by the joint set of the cascade up to now and the candidate cascade
            index, value = max(enumerate([len(final_cascade.union(set(casc))) for casc in cascades]), key=operator.itemgetter(1))
            if value>max_val:
                max_val = value
                max_seed = seed        
                max_idx = index
        
        #----- Chosen cascade for this step
        chosen_cascade = set(seed_set_cascades[max_seed][max_idx])
        
        final_cascade = final_cascade.union(chosen_cascade)
        #----- And the seed and remove it from the seed set
        seed_set.append(max_seed)
        seed_set_cascades = {seed: seed_set_cascades[seed] for seed in seed_set_cascades.keys() if seed!=max_seed }
        
    return seed_set



"""        
Main
"""
os.chdir("path\\to\\Data")

node_cascades = {}

print("loading cascades ...")

f = open("train_cascades.txt") 
idx = 0 
for line in f:
    idx+=1
    cascade = line.split(";")
    op_id = cascade[1].split(" ")[0]
    cascade = set(map(lambda x: x.split(" ")[0],cascade[2:]))
    
    if op_id in node_cascades:
        node_cascades[op_id].append(cascade)
    else:
        node_cascades[op_id] =  []
        node_cascades[op_id].append(cascade)
                
    if idx%1000==0:
        print("-----------",idx)
 
print("done with cascades, moving to  the algorithm")

start = time.time()
#S, estimated_spread = DiffusionGreedy(node_cascades,seed_no)
seed_no = 3000
S,estimated_spread = DiffusionCELF(node_cascades,seed_no)
f = open("Seed sets\\diffusion_celf_seeds.txt","w")
for i in S:
    f.write(i+" ")
f.close()    

log= open("Logs\\time_log.txt","a")
log.write("\n DiffusionCELF "+str(seed_no)+" :"+str(time.time()-start)+"\n")
log.close()


k = open("diffu_greedy_estimate.txt","w")
k.write(" "+str(estimated_spread))
k.close()