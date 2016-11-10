# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:56:15 2016

@author: Thomas
"""
import numpy as np
import itertools as it
import time


def generate_graphlets(n, gtype = 'undirected'):
    """Generate all 2- to n-nodes graphlets"""    
    # n     - number maximal of nodes to consider
    # gtype  - type of graphlet ('undirected','directed', or 'mixed')
    
    if ( gtype == 'undirected' ):
        x = [0, 2];
    elif ( gtype == 'directed' ):
        x = [-1, 0, 1];
    elif ( gtype == 'mixed' ):
        x = [-1, 0, 1, 2];
    elif ( gtype == 'labeled mixed' ):
        x = [-4,-3, 0, 2, 3, 4];
    else:
        raise NameError("The type of graphlet should be 'undirected', 'directed', or 'mixed'.");
    
    adj = []; orb = [];
    # List holding the (n-1)-nodes graphlet(s) and connections used to generate
    # the corresponding n-nodes graphlet in adj    
    origin = []; 
     
    if (n == 2):
        # Base case for 2-nodes graphlets
        if (x == [-1,0,1,2]):
            adj.append(np.array([[0, 2],[2,0]]));
            adj.append(np.array([[0, 1],[-1,0]]));
            orb.append([set([0,1])]);
            orb.append([set([0]),set([1])]);
            graphlets = [[adj,orb,[]]];
        elif (x == [-1,0,1]):
            adj.append(np.array([[0, 1],[-1,0]]));
            orb.append([set([0]),set([1])]);
            graphlets = [[adj,orb,[]]];
        elif (x == [0,2]):
            adj.append(np.array([[0, 2],[2,0]]));
            orb.append([set([0,1])]);
            graphlets = [[adj,orb,[]]]; 
        elif (x == [-4,-3, 0, 2, 3, 4]):
            adj.append(np.array([[0, 2],[2,0]]));
            adj.append(np.array([[0, 3],[-3,0]]));
            adj.append(np.array([[0, 4],[-4,0]]));
            orb.append([set([0,1])]);
            orb.append([set([0]),set([1])]);
            orb.append([set([0]),set([1])]);
            graphlets = [[adj,orb,[]]];             
    else:
        # General case for n-nodes graphlets
        graphlets = generate_graphlets(n-1,gtype);
        temp = graphlets[-1]; temp = temp[0];
        for i in range(0,len(temp)):
            M = temp[i];
            # Generate all possible connections of the new node to the 
            # (n-1)-graphlet
            for j in [p for p in it.product(x, repeat=n-1)]:
                r = np.reshape(j,(1,n-1)); 
                if np.any(r):                
                    adj.append(form_matrix(M,r));
                    origin.append([i,r]);
        intermediary = redundantNorbits(adj,n,origin);
        graphlets.append(intermediary);
    return graphlets;

##########################################################################
######################## Secondary functions #############################
    
def form_matrix(M,r):
    """Compute the matrix  0  | r
                         r' | M   
     based on vector r and Matrix M"""
    c = np.copy(r); 
    c[r == 1] = -1; c[r == -1] = 1;
    c[r == 3] = -3; c[r == -3] = 3;
    c[r == 4] = -4; c[r == -4] = 4;
    M = np.concatenate((c.T,M),axis=1);
    return np.concatenate((np.insert(r,0,0,axis=1),M),axis=0);
    
#########################################################################  
    
def redundantNorbits(adj,n,origin):
    "Remove isomorphic graphlets and store orbits"
    orb = []; adj_clean = []; origin_clean = [];
    
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
        A = adj[0]; c = count[0]; origin_clean.append([origin[0]]);
        del adj[0]; del count[0]; del origin[0];
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
            # Terminates if A was the last graphlet
            return [adj_clean,orb,origin_clean]   
            
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
            origin_clean[-1].append(origin[i]); del origin[i];
        
        print "Time elapsed :" + str(time.time()-t)        
        
    return [adj_clean,orb,origin_clean]  