# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:56:15 2016

@author: Thomas
"""
import numpy as np
import itertools as it
import time

def generate_graphlets(n,x = [-1,0,1,2]):
    """Generate all n-graphlets"""    
    # Vector x corresponds to possible edge labels 
    adj = []; orb = [];
    if (n == 2):
        # Base case for 2-graphlets
        if (x == [-1,0,1,2]):
            adj.append(np.array([[0, 2],[2,0]]));
            adj.append(np.array([[0, 1],[-1,0]]));
            orb.append([set([0,1])]);
            orb.append([set([0]),set([1])]);
            graphlets = [[adj,orb]];
        elif (x == [-1,0,1]):
            adj.append(np.array([[0, 1],[-1,0]]));
            orb.append([set([0]),set([1])]);
            graphlets = [[adj,orb]];
        elif (x == [0,2]):
            adj.append(np.array([[0, 2],[2,0]]));
            orb.append([set([0,1])]);
            graphlets = [[adj,orb]];
        else: 
            print "Error the vector x takes only three values:"
            print "         - [0,2] for undirected networks"
            print "         - [-1,0,1] for directed networks"
            print "         - [-1,0,1,2] for mixed networks"
            return -1;
    else:
        graphlets = generate_graphlets(n-1,x);
        temp = graphlets[-1]; temp = temp[0];
        for i in range(0,len(temp)):
            M = temp[i];
            # Generate all possible connections of the new node to the 
            # (n-1)-graphlet
            for j in [p for p in it.product(x, repeat=n-1)]:
                r = np.reshape(j,(1,n-1)); 
                if np.any(r):                
                    adj.append(form_matrix(M,r));
        print "Almost there..."
        graphlets.append(redundantNorbits(adj,n));
    return graphlets;

######################## Secondary functions #############################
    
def form_matrix(M,r):
    """Compute the matrix  0  | r
                         r' | M   
     based on vector r and Matrix M"""
    c = np.copy(r); 
    c[r == 1] = -1; c[r == -1] = 1;
    M = np.concatenate((c.T,M),axis=1);
    return np.concatenate((np.insert(r,0,0,axis=1),M),axis=0);
    
def redundantNorbits(adj,n):
    "Remove isomorphic graphlets and store orbits"
    orb = []; adj_clean = [];
    
    # Generate all permutations except the identity
    perm = [p for p in it.permutations(range(0,n)) if p != tuple(range(0,n))];
    
    # Count number of 1s and 2s in each graphlet
    count = [];
    for i in range(0,len(adj)):
        count.append(((adj[i]==1).sum(),(adj[i]==2).sum()));
    
    
    t = time.time();
    while len(adj)>0:
        print "Elements left: " + str(len(adj))
        # Take the first graphlet of the list
        A = adj[0]; c = count[0];
        del adj[0]; del count[0];
        adj_clean.append(A); 
        # Generate all permutations of A
        permA = []; 
        orbA = [set() for i in range(0,n)];
        for i in range(0,n):
            orbA[i].add(i);
        for i in perm:
            v = np.asarray(i); 
            temp = A[v]; temp=temp[:,v]; 
            permA.append(temp);
            # Check if any permutations are identical to A (orbits)
            if (temp == A).all():
                for j in range(0,n):
                    orbA[j].add(i[j]);
                # FOR NOW JUST STORING THE PERMUTATIONS!!!!!!!!!
                    
        orbit = [];
        while len(orbA)>0:
            o = orbA[0]; del orbA[0];
            orbit.append(o);
            if (len(orbA)==0):
                break;
            set2remove = [];
            for i in range(0,len(orbA)):
                if orbA[i].issubset(o):
                    set2remove.append(i);
            
            for i in sorted(set2remove, reverse=True): 
                del orbA[i]; 
        # Orbits are stored as list of sets of isomorphic nodes with respect
        # to the matrix representation of each graphlet (one list for each). 
        orb.append(orbit);            
        
        
        
        if (len(adj) == 0):
            # Termiates if A was the last graphlet
            return [adj_clean,orb]   
            
        # Check if any permutations is identical to one of the graphlets with
        # the distribution of edges (isomorphic graphlets)
                  
        # Retrieve graphlets that have the same type of edges
        indices = [i for i,x in enumerate(count) if x == c];    
        ind2remove = [];
        
        for i in indices:
            for j in range(0,len(permA)):
                if (adj[i] == permA[j]).all():
                    if i not in ind2remove:
                        ind2remove.append(i);
                    
        for i in sorted(ind2remove, reverse=True): 
            del adj[i]; del count[i];
    
        print "Time elapsed :" + str(time.time()-t)        
        
    return [adj_clean,orb]    