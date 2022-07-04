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
    s0 = integer_from_binary(s)
    return s0

# This function returns the keyset values that is p0, q0, r0 and s0 given the lower limit and upper limit for key
def generate_keyset(llimit = 1, ulimit = 11):

    # This key set is according to paper for diversity 
    p = np.random.randint(llimit, ulimit)
    q = np.random.randint(llimit, ulimit)
    r = np.random.randint(llimit, ulimit)
    s = get_s0(p, q, r)
    
    filename =os.path.join(os.getcwd(), "key.txt")
    with open(filename, 'w') as fp:
        fp.write(str(p) + "\n")
        fp.write(str(q) + "\n")
        fp.write(str(r) + "\n")
        fp.write(str(s) + "\n")

    return s, p, q, r

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

# This function returns an dictionary with subject number as the key and it contains the singular and minutiae point details.
def read_features(dir_path):

    mydic = {}
    key = set()
    to_remove = []

    for path in os.listdir(dir_path):
        if(os.path.isfile(os.path.join(dir_path, path))):
            file_with_extension = os.path.splitext(path)
            file_name = file_with_extension[0]
            file_extension = file_with_extension[1]
            rpath = os.path.join(dir_path, path)

            if(file_extension == ".txt" and os.path.isfile(os.path.join(dir_path, file_name + ".singular"))):
                key.add(file_name)
                file_name = file_name + "_m"
                minutiae = read_minutiae(rpath)
                mydic[file_name] = minutiae
            
            if(file_extension == ".singular" and os.path.isfile(os.path.join(dir_path, file_name + ".txt"))):
                key.add(file_name)
                new_file_name = file_name + "_s"
                singular = read_singular(rpath)
                if(len(singular) == 0):
                    to_remove.append(file_name)
                mydic[new_file_name] = singular

#   Removing the all the key when the singular file is empty i.e the length of the file is 0.
    for i in range(len(to_remove)):
        key.remove(to_remove[i])

    return mydic, key

# This function prints the dictonary in the forma key1:value1 \n key2:value2
def print_dic(dic):
    for x in dic:
        print (x,':',dic[x])

def save_template(filename, modified_list):
    filename = os.getcwd() + "/Templates/" + filename;
    
    if(not os.path.isdir(os.getcwd() + "/Templates/")):
        os.mkdir(os.getcwd() + "/Templates/")

    with open(filename, 'w') as fp:
        for item in modified_list:
            x = item[0]
            y = item[1]
            s = "%s %s\n" % (x, y)
            fp.write(s)

# This function takes minutiae list and singular point list and returns the generated template
def generate_template(singular_list, minutiae_list, s0, p0, q0, r0,a):
    n = len(minutiae_list)
    modified_minutiae_list = []
    
    for s in range(len(singular_list)):
        sx = singular_list[s][0]
        sy = singular_list[s][1]

        # We will process the minutiae point one by one i.e. we will run the algorithm one minutiae point by one minutiae point
        for i in range(n):
            dist = float('inf')
            j = -1
            xi = minutiae_list[i][0]
            yi = minutiae_list[i][1]
            # Computation of nearest location of minutiae point corresponding to current minutiae point
            for k in range(n):
                if( k != i):
                    dx = (xi-minutiae_list[k][0])*(xi-minutiae_list[k][0])
                    dy = (yi-minutiae_list[k][1])*(yi-minutiae_list[k][1])

                    dis = math.sqrt(dx + dy)
                    if(dis<dist):
                        dist = dis
                        j = k
            
            # Computation of modified location
            if(xi - minutiae_list[j][0] != 0):
                xiprime = xi + (p0*math.cos(math.radians(q0) + math.atan( (yi-minutiae_list[j][1]) / (xi-minutiae_list[j][0]) ) ) )
                yiprime = yi + (p0*math.sin(math.radians(q0) + math.atan( (yi-minutiae_list[j][1]) / (xi-minutiae_list[j][0]) ) ) )
            else:
                xiprime = xi + (p0*math.cos(math.radians(q0) + math.atan( float('inf') ) ) )
                yiprime = yi + (p0*math.sin(math.radians(q0) + math.atan( float('inf') ) ) )

            # Reducing translation due to intra-subject variance
            xiprime = xiprime - sx
            yiprime = yiprime - sy

            # Security enhancement of the user template
            t1 = xiprime*math.cos(math.radians(q0)) - yiprime*math.sin(math.radians(q0))
            t2 = xiprime*math.sin(math.radians(q0)) + yiprime*math.cos(math.radians(q0))
            xiprime = t1
            yiprime = t2

            xiprime = xiprime + s0*math.cos(math.radians(r0))
            yiprime = yiprime + s0*math.sin(math.radians(r0))
            modified_minutiae_list.append((xiprime, yiprime))

        save_file_name = a + "_" + str(s)
        save_template(save_file_name, modified_minutiae_list)

# This function generates the secured template for fingerprint 
def generate_secured_template(database = "Database"):
    dic, key = read_features(database)
    key = sorted(key)

    s0, p0, q0, r0 = generate_keyset(4, 41)
    for a in key:
        minutiae = a + "_m"
        singular = a + "_s"

        minutiae_list = dic[minutiae]
        singular_list = dic[singular]
        generate_template(singular_list, minutiae_list, s0, p0, q0, r0, a)

        # n = len(minutiae_list)
        # modified_minutiae_list = []
        
        # for s in range(len(singular_list)):
        #     sx = singular_list[s][0]
        #     sy = singular_list[s][1]

        #     # We will process the minutiae point one by one i.e. we will run the algorithm one minutiae point by one minutiae point
        #     for i in range(n):
        #         dist = float('inf')
        #         j = -1
        #         xi = minutiae_list[i][0]
        #         yi = minutiae_list[i][1]
        #         # Computation of nearest location of minutiae point corresponding to current minutiae point
        #         for k in range(n):
        #             if( k != i):
        #                 dx = (xi-minutiae_list[k][0])*(xi-minutiae_list[k][0])
        #                 dy = (yi-minutiae_list[k][1])*(yi-minutiae_list[k][1])

        #                 dis = math.sqrt(dx + dy)
        #                 if(dis<dist):
        #                     dist = dis
        #                     j = k
                
        #         # Computation of modified location
        #         if(xi - minutiae_list[j][0] != 0):
        #             xiprime = xi + (p0*math.cos(math.radians(q0) + math.atan( (yi-minutiae_list[j][1]) / (xi-minutiae_list[j][0]) ) ) )
        #             yiprime = yi + (p0*math.sin(math.radians(q0) + math.atan( (yi-minutiae_list[j][1]) / (xi-minutiae_list[j][0]) ) ) )
        #         else:
        #             xiprime = xi + (p0*math.cos(math.radians(q0) + math.atan( float('inf') ) ) )
        #             yiprime = yi + (p0*math.sin(math.radians(q0) + math.atan( float('inf') ) ) )

        #         # Reducing translation due to intra-subject variance
        #         xiprime = xiprime - sx
        #         yiprime = yiprime - sy

        #         # Security enhancement of the user template
        #         t1 = xiprime*math.cos(math.radians(q0)) - yiprime*math.sin(math.radians(q0))
        #         t2 = xiprime*math.sin(math.radians(q0)) + yiprime*math.cos(math.radians(q0))
        #         xiprime = t1
        #         yiprime = t2

        #         xiprime = xiprime + s0*math.cos(math.radians(r0))
        #         yiprime = yiprime + s0*math.sin(math.radians(r0))
        #         modified_minutiae_list.append((xiprime, yiprime))

        #     save_file_name = a + "_" + str(s)
        #     save_template(save_file_name, modified_minutiae_list)

def main():
    generate_secured_template("Database")

# Main function calling
if __name__ == "__main__":
    main()