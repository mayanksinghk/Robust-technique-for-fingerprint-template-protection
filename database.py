#!/usr/bin/env python3
"""
This python script will perform the following task:
1) Read the minutiae points from .txt file and singular points from .singular points
2) Secured template generation
3) Save the generated template in a database with key as the subject number, finger number, singular point number

"""

import numpy as np
import os
import math

def integer_from_binary(b):
    ans = 0
    for i in range(48):
        if(b[i] == '1'):
            ans = ans + pow(2, 47-i)
     

    return ans;

# This function returns the value of s0. The s0 is an 48 bit length binary string which is converted to an integer value with the help of function integer_from_binary(b).
def get_s0(p, q, r):
    s = bin(math.floor(p))[2:19].zfill(16) + bin(math.floor(q))[2:19].zfill(16) + bin(math.floor(r))[2:19].zfill(16)
    s0 = integer_from_binary(s0)
    return s

# This function returns the keyset values that is p0, q0, r0 and s0 given the lower limit and upper limit for key
def generate_keyset(llimit = 1, ulimit = 11):

    # This key set is according to paper for diversity 
    p0 = np.random.randint(llimit, ulimit)
    q0 = np.random.randint(llimit, ulimit)
    r0 = np.random.randint(llimit, ulimit)
    s0 = get_s0(p0, q0, r0)
    
    return s0, p0, q0, r0

def generate_secured_template():
    pass


def save_template(snum, fnum, singnum):
    pass


# This function returns an dictionary with subject number as the key and it contains the singular and minutiae point details.
def read_features(dir_path):

    mydic = {}
    
    for path in os.listdir(dir_path):
        if(os.path.isfile(os.path.join(dir_path, path))):
            file_with_extension = os.path.splitext(path)
            file_name = file_with_extension[0]
            file_extension = file_with_extension[1]
            rpath = os.path.join(dir_path, path)

            if(file_extension == ".txt"):
                file_name = file_name + "_m"
                minutiae = read_minutiae(rpath)
                mydic[file_name] = minutiae
            
            if(file_extension == ".singular"):
                file_name = file_name + "_s"
                singular = read_singular(rpath)
                mydic[file_name] = singular

    return mydic


# This function reads the all the minutiae points in a file(extension of the file should be .txt) and returns a list containing all the minutiae points
def read_minutiae(file_name):
    # Check if the file is correct that is the extenstion of the file is .text
    file_with_extension = os.path.splitext(file_name)
    f_name = file_with_extension[0]
    f_extension = file_with_extension[1]

    if(f_extension != ".txt"):
        raise TypeError("The extension of the input file is not .txt which is standard for minutiae points file")

    m_points = []

    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            temp = line.split()
            x,y,d = temp[0],temp[1],temp[2]
            x,y = float(x),float(y)
            theta = math.radians(float(d))
            m_points.append([x,y,theta])
            
    return m_points

# This function reads the all the singular points in a file(extension of the file should be .singular) and returns a list containing all the singular points
def read_singular(file_name):
    # Check if the file is correct that is the extenstion of the file is .singular
    file_with_extension = os.path.splitext(file_name)
    f_name = file_with_extension[0]
    f_extension = file_with_extension[1]

    if(f_extension != ".singular"):
        raise TypeError("The extension of the input file is not .singular which is standard for singular points file")

    s_points = []

    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            temp = line.split()
            x,y = temp[0],temp[1]
            x,y = float(x),float(y)
            s_points.append([x,y])
            
    return s_points

# This function prints the dictonary in the forma key1:value1 \n key2:value2
def print_dic(dic):
    for x in dic:
        print (x,':',dic[x])

# generate_keyset()

dic = read_features(dir_path="Database")
# print_dic(dic)