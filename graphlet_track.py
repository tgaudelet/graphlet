# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 15:33:26 2016

@author: Thomas
"""

import numpy as np


class graphlet:
    def __init__(self,ID,n,A,orbit,posteriors):
        self.id = ID;
        self.num_node = n;
        self.adj = A;
        self.orbit = orbit;
        self.posteriors = posteriors;
        
    def add_posterior(self,posterior):
        self.posteriors.append(posterior);
        
        
        

def graphlet_track(n,gtype = "mixed"):
    """Funtion return a structure giving which k-nodes graphlets you can get 
       from a given (k-1)-nodes graphlet and how"""
    track = []; # List of dictionaries   
    k = 0;
    # Step 1: generate the graphlets
    graphlets = generate_graphlets(n,gtype);
    for i in range(0,len(graphlets)):
        temp = graphlets[i]; 
        adj = temp[0]; orb = temp[1]; origin = temp[2];
        if i == 0:
            ll = 0;
        else:
            ll = len(graphlets[i-1][0]);
        for j in range(0,len(adj)):
            orbit = np.zeros(i+2);
            for sset in orb[j]:
                for jj in sset:
                    orbit[jj] = k;
                k += 1;
            track.append(graphlet(j+ll,i+2,adj[j],orbit,[]));
            if origin:
                cur = origin[j];
                if i == 1:
                    ll = 0;
                else:
                    ll = len(graphlets[i-2][0]);                
                for ii in range(0,len(cur)):
                    curr = cur[ii];
                    track[curr[0]+ll].add_posterior([curr[1],j]);
                        
    return track;
        
#T = graphlet_track(4);
f = open("graphlets.txt","w");
for i in range(0,len(T)):
    f.write("{ \n");
    f.write("#Graphlet ID:\n")
    f.write(str(T[i].id)+"\n");
    f.write("#Graphlet Number of node:\n")
    f.write(str(T[i].num_node)+"\n");
    f.write("#Graphlet Orbit:\n")
    temp = T[i].orbit;
    for j in temp:
        f.write(str(int(j))+ " ");
    f.write("\n");    
    f.write("#Graphlet Adjacency Matrix:\n")
    temp = T[i].adj;
    f.write(str(len(temp))+" " +str(len(temp[0]))+"\n");
    for k in range(0,len(temp)):
        for j in range(0,len(temp[k])):
            f.write(str(temp[k][j]) + " ");
        f.write("\n");
    f.write("#Graphlet Posteriors:\n")
    temp = T[i].posteriors;
    f.write( str(len(temp)) + "\n" );
    for k in range(0,len(temp)):
        for j in range(0,len(temp[k][0])):
            f.write(str(temp[k][0][j]) + " ");
        f.write(str(temp[k][1])+"\n");
    f.write("}\n");

f.close();