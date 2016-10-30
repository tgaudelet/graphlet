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
    n = len(graphlets); 
    pdf = matplotlib.backends.backend_pdf.PdfPages(name+".pdf")
      
    
    for i in range(0,n):
        adj = graphlets[i][0]; 
        for j in range(0,len(adj)): 
            print "Graphlet " + str(j+1) + " of " + str(len(adj));
            t = time.time();   
            A = adj[j];
            orbits = graphlets[i][1][j];
            draw_graph_from_adj(A,orbits);
            pdf.savefig(plt.gcf(),bbox_inches='tight')
            plt.clf()
            print "Time elapsed: " + str(time.time() - t);
    plt.close()        
    pdf.close()

######################### Secondary functions ################################

def draw_graph_from_adj(A,orb,dist=5):
    n = len(A); m = len(orb);
    theta = 2*math.pi/n;   
    radius = dist/5;
    
    r = dist/(2*math.sin(math.pi/n));
    nodes = [(-r,0)];
    current_node = nodes[0];
    c = math.cos(theta); s = math.sin(theta);
    for i in range(1,n):
        x = c*current_node[0] + s*current_node[1];         
        y = c*current_node[1] - s*current_node[0];
        current_node = (x,y);
        nodes.append(current_node);
            
    colors = _get_colors(m);
    ax = plt.axes()
    for i in range(0,n):
        for j in range(0,m):
            if i in orb[j]:            
                plt.gca().add_patch(plt.Circle(nodes[i] , radius, fc=colors[j]))

    
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
#    plt.savefig("test.pdf", bbox_inches='tight')
#    plt.show() 
#    return ax;

def _get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors
