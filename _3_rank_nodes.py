# -*- coding: utf-8 -*-
"""
@author: georg

Take the top 3000  nodes ranked based on each feature and store it to be used for NETRATE
Take the top 100 based on each feature and store it as seed set.
"""

import os            
import pandas as pd

"""
Main
"""
os.chdir("path\\to\\Data")

dat = pd.read_csv("node_features.csv")

#------ Take the top 0.5%~=3000 seeds based on degree and store it in each column of top
perc = 3000
top = pd.DataFrame(columns=dat.columns)
col="Degree"
top[col] = dat.nlargest(perc,col)["Nodes"].values

top = top.drop(["Nodes"], axis=1)  

#------ Store the node ids of the top 3000 nodes for each feature
top.to_csv("top_nodes.csv",index=False)

#------ Store as seed sets the top 100 of each feature
c = "Kcores"
f = open("Seeds\\centr_"+c.lower()+"_seeds.txt","w")
f.write(" ".join([str(x) for x in list(top.loc[0:100,c].values)]))
f.close()
