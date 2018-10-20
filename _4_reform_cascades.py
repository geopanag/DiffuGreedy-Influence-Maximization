# -*- coding: utf-8 -*-
"""
@author: georg

Reform the training cascades to serve as input to NETRATE
Remove nodes in the cascades that do not belong to the top 3000 (for each feature)
"""

import os
import time
import pandas as pd
from datetime import datetime

#---- The relative timestamp is the offset with respect to the start of the recording
reference_timestamp = datetime.strptime('2012-09-28-00:00:00','%Y-%m-%d-%H:%M:%S')


def get_timestamp(real_time):
    """
    #Given real timestamp of a retweet, return the relative timestamp
    """
    return str(int((datetime.strptime(real_time, '%Y-%m-%d-%H:%M:%S') - reference_timestamp).total_seconds()))


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


"""
Main
"""
os.chdir("path\\to\\Data")

log= open("Logs\\time_log.txt","a")

top = pd.read_csv("top_nodes.csv")
cols = top.columns

for col in cols:
    start  = time.time()
    top_c = list(top[col].values)
    #------ Node ids in netrate input file must belong to 1:3000
    top_dict ={b:v for v,b in enumerate(top_c)} 
    
    f = open("train_cascades.txt")
    
    idx = 0
    cascades = []
    
    #------ Go through all cascades to reform and filter them
    for line in f:
        cascade = line.replace("\n","").split(";")[1:]
        cascade_nodes = []
        cascade_times = []
        for c in cascade[1:]:
            uid = int(c.split(" ")[0])
            
            #---- Filter each cascade to contain only top nodes for feature col
            if uid in top_c:
                cascade_nodes.append(top_dict[uid])        
                cascade_times.append(get_timestamp(c.split(" ")[1])) 
        
        if len(cascade_nodes)<=1:
            continue
        
        #---- Some cascades have duplicate retweets
        cascade_nodes, cascade_times = remove_duplicates(cascade_nodes,cascade_times)
        
        #---- Set it in the right format to be read by netrate
        cascades.append(",".join([str(v) + "," + cascade_times[i] for i,v in enumerate(cascade_nodes)]))
            
        idx+=1
        if(idx%100==0):
            print("-------------------",idx)
                
    f.close()
    
    #------Write first the extracted ids and then the cascades
    g = open("Netrat\\cascades_"+col.lower()+".txt","w") 
    for i in top_dict:
        g.write(str(top_dict[i])+","+str(top_dict[i])+"\n")
    g.write("\n")
    
    for c in cascades:
        g.write(c+"\n")
    g.close()
     
    log.write("Time to prepare data for NetRate, feature "+col+" :"+str(time.time()-start)+"\n")   

log.close()

    
    
    
