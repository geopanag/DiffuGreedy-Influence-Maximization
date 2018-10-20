# -*- coding: utf-8 -*-
"""
@author: georg

Extract the user ids of the nodes that are actively retweeting during the time span of
the follower network. Extract the train and test cascades. 
Filter the graph to contain only these nodes.
"""

import os
import time

def split_train_and_test(cascades_file):
    """
    # Splits the cascades into those that start before and after the 25th day of recording
    # Keeps the ids of the users that are actively retweeting
    """
    f = open(cascades_file)
    ids = set()
    train_cascades = []
    test_cascades = []
    counter = 0
    
    for line in f: 
        
        date = line.split(" ")[1].split("-")
        original_user_id = line.split(" ")[2]
        
        retweets = f.next().replace(" \n","").split(" ")
        #----- keep only the cascades and the nodes that are active at 2012.9.28 to 2012.10.29.     
        if int(date[0])==2012:
           
           retweet_ids = ""
           #------- last 7 days kept for testing
           if int(date[1])==10 and int(date[2])>=23 and int(date[2])<=29: 
               ids.add(original_user_id)           
               cascade = ""
               for i in range(0,len(retweets)-1,2):
                   ids.add(retweets[i])
                   retweet_ids = retweet_ids+" "+retweets[i]
                   cascade = cascade+";"+retweets[i]+" "+retweets[i+1]
                   
               #------- For each cascade keep also the original user and the relative day of recording (1-32)
               date = str(int(date[2])+3)
               op = line.split(" ")
               op = op[2]+" "+op[1]
               test_cascades.append(date+";" +op+cascade)
        
           #------ The rest of the days are used for training
           elif int(date[1])==10 or (int(date[1])==9 and int(date[2])>=28):
               ids.add(original_user_id)          
               cascade = ""          
               for i in range(0,len(retweets)-1,2):
                   ids.add(retweets[i])
                   retweet_ids = retweet_ids+" "+retweets[i]
                   cascade = cascade+";"+retweets[i]+" "+retweets[i+1]
               if(int(date[1])==9):
                   date = str(int(date[2])-27)
               else:
                   date = str(int(date[2])+3)
               op = line.split(" ")
               op = op[2]+" "+op[1]
               train_cascades.append(date+";" +op+cascade)
               
        counter+=1    
        if (counter % 100000==0):
            print("------------"+str(counter))
    f.close()
    
    return train_cascades, test_cascades, ids 




"""
Main
"""
os.chdir("path\\to\\Data")

log= open("Logs\\time_log.txt","a")

start = time.time()

#------ Split the original retweet cascades
train_cascades, test_cascades, ids  = split_train_and_test("Init_Data\\total.txt")

#------ Store the cascades
print "Size of train:",len(train_cascades)
print "Size of test:",len(test_cascades)

with open("train_cascades.txt","w") as f:
    for cascade in train_cascades:
        f.write(cascade+"\n")

with open("test_cascades.txt","w") as f:
    for cascade in test_cascades:
        f.write(cascade+"\n")

#------- Keep the processing time
log.write("Cascade extraction time :"+str(time.time()-start)+"\n")

start = time.time()

#------ Store the active ids
f = open("active_users.txt","w")
for uid in ids:
    f.write(uid+"\n")
f.close()


#------ Keep the subnetwork of the active users
g = open("active_network.txt","w")

f = open("Init_Data\\graph_170w_1month.txt")

found =  0
idx=0
for line in f:
    edge = line.split(" ")
    
    if edge[0] in ids and edge[1] in ids:
        found+=1
        g.write(line)
    idx+=1    
    if (idx%1000000==0):
        print(idx)

f.close()
g.close()

log.write("Filtering of follower graph :"+str(time.time()-start)+"\n")
log.close()

