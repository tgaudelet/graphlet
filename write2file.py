# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 09:15:07 2016

@author: Thomas
"""

import pickle

def write2file(DD, name = "5-graphlets"):
    
    with open(name+".pkl",'wb') as file:
       pickle.dump(DD,file);
       
       
def read_from_file(path):
    
    with open(path,"rb") as file:
        new_variable = pickle.load(file);
        
    return new_variable
            