# DiffuGreedy Influence Maximization
Code and instructions to reproduce the analysis of the paper [DiffuGreedy: An Influence Maximization Algorithm Based on Diffusion Cascades](https://link.springer.com/chapter/10.1007/978-3-030-05411-3_32)

## Folder structure
Root folders: Code, Data, Figures

Code: Contains the contents of this folder and the code of [NETRATE](people.tuebingen.mpg.de/manuelgr/netrate/#code). You will also need code for [IMM](https://sourceforge.net/projects/im-imm/) and [SIMPATH](https://www.cs.ubc.ca/~goyal/code-release.php). 
PMIA.py and runIAC.py are taken from python [PMIA implementation](https://github.com/nd7141/influence-maximization/tree/master/IC). 

Data -> Init Data: Contains the cascades and the follower network from [Sina Weibo](https://aminer.org/influencelocality) i.e. total.txt and graph_170w_1month.txt <br> 
Data ->Empty folder Logs <br>
Data ->Empty folder Netrate <br>
Data ->Empty folder Seeds <br>
Data ->Empty folder Results <br>

## Requirements
gcc version >=4.7

MATLAB 2017b

Python 2.7, packages:
igraph, pandas, numpy, networkx

R packages :ggplot, reshape2


## Code
The scripts follow the order indicated by the number in their title. <br>
Below is an explanation on how each influence maximization technique is implemented through the scripts. 


### Diffusion Greedy
- \_2\_diffusion\_greedy.py runs diffusion-based influence maximization using the train cascades.

### Ranking by K-core decomposition
- \_2\_train.py runs k-core decomposition for each node in the active graph and stores it at kcores.csv. 
- \_3\_rank\_nodes.py derives the top nodes based on it and stores them at folder Seeds. 

### Influence Maximization via Martingales
- \_2\_train.py extracts the active network for the first 25 days at train\_network.pickle.
- \_3\_extract\_weighted\_cascade.py adds edge weights to the network based on weighted cascade and stores it at follower\_weighted.txt. It also creates the attribute file required for the IMM algorithm.
- Use the IMM code to produce the seed set of follower\_weighted.txt  and store it in a file with the same name in Data\Seeds.

### PMIA on the Diffusion-based Network
- \_4\_reform\_cascades.py uses top\_nodes.csv created by \_3\_rank\_nodes.py to filter the training cascades to include only top nodes based on degree and follow the format required for NETRATE. The cascade file is stored at Data\Netrate.
- \_5\_call\_netrate.m calls NETRATE algorithm for each cascade file and stores the resulting adjacency list at Data\Netrate.
- \_6\_run\_pmia.py creates a network out of the adjecency matrix, weighs it based on weighted cascade and computes NETRATE's accuracy in retrieving follow relationships. It then uses PMIA to derive the seed set.

### SIMPATH on the Data-based weighted Network
- \_2\_train.py extracts the active network for the first 25 days at train\_network.pickle.
- \_3\_extract\_bernouli\_and\_time.py extracts three weighted networks, with edge weights based on influence strength (literature's Bernoulli-ic), the inverse of average influence delay, and their product. 
- Use the SIMPATH code and the .inf files from the previous step to derive the seed sets and store them in text files with the same name as the .inf, with format "seed1 seed2 seed3 etc..", in Data\Seeds.


**License**

- [MIT License](https://github.com/geopanag/DiffuGreedy-Influence-Maximization/blob/master/LICENSE)
