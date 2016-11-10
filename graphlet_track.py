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
        


def graphlet_track(n,gtype = "labeled mixed",save = 0):
    """Funtion return a structure giving which k-nodes graphlets you can get 
       from a given (k-1)-nodes graphlet and how"""
    track = []; # List of dictionaries   
    post = init_list_of_objects(3);
    k = 0;
    # Step 1: generate the graphlets
    graphlets = generate_graphlets(n,gtype);
    for i in range(0,len(graphlets)):
        temp = graphlets[i];
        adj = temp[0]; orb = temp[1]; origin = temp[2];
        if i == 0:
            l = 0;
        else:
            if i == 1:
                l = 3;
            else:
                l = 43;
        for j in range(0,len(adj)):
            orbit = np.zeros(i+2);
            for sset in orb[j]:
            # associate each element in the graphlet with its orbit
                for jj in sset:
                    orbit[jj] = int(k);
                k += 1;
            
            # Create the new graphlet
            track.append(graphlet(j+l,i+2,adj[j],orbit,[]));
            
            # Find which graphlet can be obtained from a smaller one based on origin structure
            if origin:
                cur = origin[j];
                if i == 1:
                    ll = 0;
                else:
                    ll = len(graphlets[i-2][0]);    
                    
                for ii in range(0,len(cur)):
                    curr = cur[ii];
                    post[curr[0]+ll].append([curr[1],j+l]);
                    
    # Cleaning up the posteriors structure and adding it to class instances
    for j in range(0,3):
        p = post[j];
        for i in range(0,len(p)):
            connection = p[i][0]; graph = p[i][1];
            cg = track[j]; orb = cg.orbit;
            transf = [];  
            for ii in range(0,len(connection[0])):
                k = connection[0][ii];
                if (k == 2):
                    # connected_orb (connected graphlet, orbits connected)
                    connected_orb = (0,int(orb[ii]),0);
                    transf.append(connected_orb);
                elif (k == -3):
                    connected_orb = (1,int(orb[ii]),1);
                    transf.append(connected_orb);
                elif (k == 3):
                    connected_orb = (1,int(orb[ii]),2);
                    transf.append(connected_orb);
                elif (k == -4):
                    connected_orb = (2,int(orb[ii]),3);
                    transf.append(connected_orb);
                elif (k == 4):
                    connected_orb = (2,int(orb[ii]),4);
                    transf.append(connected_orb);
            transf.append(graph);
            post_c = cg.posteriors; 
            if post_c:
                boo = 0;
                for kk in range(0,len(post_c)):
                    if (len(transf) != len(post_c[kk])):
                        continue;
                    else:
                        for b in range(0,len(transf)):
                                if transf[b] not in post_c[kk]:
                                    boo = 0;
                                    break;
                                else:
                                    boo = 1;
                           
                    if boo == 1:
                        break;
                if boo == 0:
                    cg.add_posterior(transf);
            else:
                cg.add_posterior(transf);
    # Saving to a file        
    if save:
        f = open("graphlets.glts","w");
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
                for j in temp[k]:
                    f.write(str(j) + " ");
                f.write("\n");
            f.write("}\n");
        
        f.close();
            
                  
    return track;
     
     
def init_list_of_objects(size):
    list_of_objects = list()
    for i in range(0,size):
        list_of_objects.append( list() ) #different object reference each time
    return list_of_objects    
    
T = graphlet_track(3,save=1);