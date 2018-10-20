# -*- coding: utf-8 -*-
"""

@author: georg

Simpath imlementation as is described in Goyal 2011, without the two optimizations
"""


import os
import time
import glob
from igraph import *


class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def add(self, item):
         self.items.append(item)

     def last(self):
         return self.items[len(self.items)-1]
     
     def size(self):
         return len(self.items)


def forward(Q,D,spd,pp,threshold,W,g):    
    """
    Forward from Goyal 2011
    DFS in W (V-S+u)
    """
    
    x = Q.last()
    edges = g.es[g.incident(x, mode="out")]
    
    if x not in D:
        D[x]=[]
    
    for edge in edges:   
        y = edge.tuple[1]
        
        #----- Checks whether:
        # the edge is repeated, using D[x]
        # the node is already in the stack for search using Q (refrain from cycles)
        # the node is not a seed, using W
        if (y not in Q.items) and (y not in D[x]) and y in W:
            #print(str(edge.tuple[0])+" "+str(edge.tuple[1])+" "+str(pp)+" "+str(edge["weight"]))
            #----- If the path probability falls under the threshold, do not add it
            if(pp*edge["weight"]<threshold):
                D[x].append(y)
            else:
            #----- If it s ok, add the new node to stack and DFS from it
                Q.add(y)
                pp =  pp*edge["weight"]
                #----- The total influence spread ammounts to the probability of all paths from u
                spd += pp
                
                D[x].append(y)
                #---- x changes so DFS goes one level deeper
                Q,D,spd,pp = forward(Q,D,spd,pp,threshold,W,g)
                break

    return Q,D,spd,pp


def backtrack(u,threshold,W,g):
    """
    Backtrack from Goyal 2011
    
    Enumerate all simple paths in W starting from u with DFS and cutof at threshold
    pp = weight of current path
    spd = total spread of u
    Q = nodes in the path
    D[x] = out neighbors of node x that have been visited
    """
    pp = 1
    spd =  1
    Q = Stack()
    Q.add(u)
    D = {}
    
    while(Q.size()>0):
         Q,D,spd,pp = forward(Q,D,spd,pp,threshold,W,g)   
         #------ 
         u =  Q.last()
         Q.items.remove(u)
         del D[u]
         if Q.size()==0:
             break
         v = Q.last()
         
         
         pp = pp/g.es[g.get_eid(v,u)]["weight"] 
         
    return spd            


def simpath_spread(W,S,threshold,g):
    """
    Simpath Spread from Goyal 2011
    """
    
    sigma = 0 #{s:0 for s in S}
    for u in S:
        #----- u,h,V-S+u
        sigma += backtrack(u,threshold,W.union(set([u])),g)  
    return sigma
  
    
def celf(g,k=100,threshold = float(1)/10000):
    """
    CELF with simpath spread
    """  
    S = set()
    
    #---- The nodes that do not belong to the seed set
    W = range(0,len(g.vs["name"]))
    
    spreads = [0 for v in W]
    
    while len(S)<k:
        print("-----------:",len(S))
        boo = False
        
        #------------------------------
        for i,v in enumerate(W):
            #spreads[i] = simpath_spread(V,S.union(set([v])),threshold)
            spreads[i] = simpath_spread(set(W),S.union(set([v])),threshold,g)
            
            if(i==(len(W)-1)):
                break
            
            #------ Celf trick, only after the first iteration
            if(spreads[i]>spreads[i+1] and len(S)>0):
                boo = True
                S.add(v)
                del W[i]
                del spreads[i]
                break
            
        #---- The best seed was found by the celf trick
        if boo:
            continue
        
        #------Sort the nodes by influence spreads
        W = [x for _,x in sorted(zip(spreads,W),reverse=True)]
        spreads = sorted(spreads)
        
        #------ Keep the node with the highest marginal gain
        S.add(W[0])
        del W[0]
        del spreads[0]
        
    return S
    
    
