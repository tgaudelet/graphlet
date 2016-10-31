# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 19:15:43 2016

@author: Thomas
"""

import matplotlib.backends.backend_pdf
import numpy as np
import matplotlib.pyplot as plt
import math 
import colorsys
import time

def draw_graphlets(graphlets,name):
    " Draw the graphlets in the structure to the file name.pdf "
    # graphlets  - structure holding the adjencency matrices and orbits set of 
    #              each graphlet
    # name       - name of the pdf file where the graphlet figure are to be saved
    
    n = len(graphlets); 
    orbit_counter = 1; # To numerote orbits in the representation
    #   Open pdf page
    pdf = matplotlib.backends.backend_pdf.PdfPages(name+".pdf")
      
    for i in range(0,n):
        adj = graphlets[i][0]; 
        for j in range(0,len(adj)): 
            print "Graphlet " + str(j+1) + " of " + str(len(adj));
            t = time.time();   
            A = adj[j];
            orbits = graphlets[i][1][j];
            # Drawing a graphlet and saving it to the file
            orbit_counter = draw_graph_from_adj(A,orbits,orbit_counter);
            pdf.savefig(plt.gcf(),bbox_inches='tight')
            plt.clf()
            print "Time elapsed: " + str(time.time() - t);
    plt.close()        
    pdf.close()
    return orbit_counter

##########################################################################
######################### Secondary functions ############################
##########################################################################

def draw_graph_from_adj(A,orb,orbit_counter,dist=5):
    """Draw the graphlet given by adjacency matrix A and orbit orb with distance
      dist between the node"""
    # A    - adjacency matrix of the graphlet
    # orb  - set(s) of orbits of the graphlet
    # dist - distance between the nodes in our drawing

    n = len(A); m = len(orb);  
    radius = dist/5; # radius of the circles representing the nodes
    
    # Step 1: place nodes in space on a circle at equal distance
    theta = 2*math.pi/n; 
    r = dist/(2*math.sin(math.pi/n));
    nodes = [(-r,0)];
    current_node = nodes[0];
    c = math.cos(theta); s = math.sin(theta);
    for i in range(1,n):
        x = c*current_node[0] + s*current_node[1];         
        y = c*current_node[1] - s*current_node[0];
        current_node = (x,y);
        nodes.append(current_node);
        
    # Step 2: generate as many colors as there are orbits sets.        
    colors = get_colors(m);
    
    # Step 3: plot all the nodes with color corresponding to their orbit
    ax = plt.axes()
    for j in range(0,m):
        for i in range(0,n):
            if i in orb[j]:            
                plt.gca().add_patch(plt.Circle(nodes[i] , 
                                    radius, 
                                    fc=colors[j]));
                ax.annotate(str(orbit_counter), xy=nodes[i], xycoords="data",
                  va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=colors[j], ec="none",));
                
        orbit_counter += 1;

    # Step 4: Draw the edges depending on value in adjacency matrix
    for i in range(0,n-1):
        for j in range(i+1,n):
            temp = A[i][j];
            
            if (temp == 0): 
                continue;
                
            xi = nodes[i][0]; xj = nodes[j][0];
            yi = nodes[i][1]; yj = nodes[j][1];
            nv = math.sqrt((xi-xj)**2 + (yi-yj)**2); 
            vx = radius*(xi-xj)/nv; vy = radius*(yi-yj)/nv;
            
            
            if (temp == 2):
                pad = 0.1;
                xx = (xi-(1+pad)*vx,xj + (1+pad)*vx);
                yy = (yi-(1+pad)*vy,yj + (1+pad)*vy);
                edge = plt.Line2D(xx, yy, color = 'k',
                                  markeredgecolor='k',
                                  markerfacecolor='k');
                plt.gca().add_line(edge);
                
            elif (temp == 1):
                ax.annotate("",
                            xy=(xj+vx,yj+vy), xycoords='data',
                            xytext=(xi-vx,yi-vy), textcoords='data',
                            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
                            )
                            
            elif (temp == -1):
                ax.annotate("",
                            xy=(xi-vx,yi-vy), xycoords='data',
                            xytext=(xj+vx,yj+vy), textcoords='data',
                            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
                            )       
        

    plt.axis('scaled')
    plt.axis('off')
    return orbit_counter
    
##########################################################################

def get_colors(num_colors):
    "generate num_colors colors"
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors
