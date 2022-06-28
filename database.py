#!/usr/bin/env python3
"""
This python script will perform the following task:
1) Read the minutiae points from .txt file and singular points from .singular points
2) Secured template generation
3) Save the generated template in a database with key as the subject number, image number, singular point number

"""

import numpy as np
import sys 
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


def read_features():
    pass


def read_minutiae():
    pass


def read_singular():
    pass


generate_keyset()