#!/usr/bin/env python3

"""
This python script will implement following functionalities:
1) Perform one to one matching between query and a template stored in database. 
2) Perform one to many matching between query and templates stored in database.

Both of the function will return the matching score(highest matching score in case of one to many) which will be calculated as
    matching score = ((min(mns/ns, mnq/nq))*100)
"""

import template as tp
import numpy as np
import os
import math
import cv2

"""
Things to do in Matching:
[x] Input to file is the name of query fingerprint example: 101_1.png
[x] Check if singular file is valid(present and non-empty)
[x] Create the template for the fingerprint by selecting singular point closer to center of the image.
[] Calculate hausdroff distance between every point in query with stored template and vice versa and the point is matched if the hausdroff dis is less than a threshold(T1)
[] Now rotate the query template from -60 to 60 degrees 1 degree at a time to remove rotation invariant.
[] Calculate matching score for each rotated query template and template stored in database. 
[] Max out the matching score and compare it with the threshold(T2 or T) to know if the query and stored template is matched or not.
[] Repeat this process for every stored template to get the exact result.
"""

# This function checks if the given name of th singular file is valid or not
def check_singular_file(s):
    if( not os.path.isdir("Database")):
        print("The database is not present in the working directory")
        print("Please import the database to folder where the python script is running and name the directory \"Database\" ")
        return False
    else:
        if(not os.path.isfile(os.path.join("Database" , s))):
            print("The singular file is not present in the database")
            return False
        else:
            s_points = []
            file_name = os.path.join("Database" , s)
            with open(file_name) as f:
                lines = f.readlines()
                for line in lines:
                    temp = line.split()
                    x,y = temp[0],temp[1]
                    x,y = float(x),float(y)
                    s_points.append([x,y])
            
            if(len(s_points) == 0):
                print("The singular file is present but empty")
                return False
            else:
                return True

# This function is takes the name of the fingerprint and creates the template for the query image
def query_template(qimage):
    

    file_with_extenstion = os.path.splitext(qimage)
    file_name = file_with_extenstion[0]
    singular_file = file_name + ".singular"
    minutiae_file = file_name + ".txt"


    im = cv2.imread(os.path.join("Database" , qimage))
    height, width = im.shape[0:2]
    centerx, centery = int(height//2), int(width//2)
    sx, sy = 0, 0
    min = np.inf
    minutiae_list = []

    check = check_singular_file(singular_file)
    print(singular_file)
    if(check == False):
        print("The singular file is not valid")
        exit()
    else:
        file_name = os.path.join("Database" , singular_file)
        with open(file_name) as f:
            lines = f.readlines()
            for line in lines:
                temp = line.split()
                x,y = float(temp[0]),float(temp[1])
                dist = math.sqrt((x-centerx)*(x-centerx) + (y-centery)*(y-centery))
                if(dist < min):
                    min = dist
                    sx = x
                    sy = y
    
        file_name = os.path.join("Database" , minutiae_file)
        with open(file_name) as f:
            lines = f.readlines()
            for line in lines:
                temp = line.split()
                x,y,d = temp[0],temp[1],temp[2]
                x,y = float(x),float(y)
                theta = math.radians(float(d))
                minutiae_list.append([x,y,theta])

        
        # Get the keyset from the file key.txt
        s, p, q, r = tp.read_keyset()

        # generate the template for query image
        file_name = file_with_extenstion[0]
        tp.generate_template(sx, sy, minutiae_list, s, p, q, r, file_name)

    return 0

# This function rotates the input set of points by a certain degrees
def rotate(p, origin=(0, 0), degrees=0):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((np.dot(R, (p.T-o.T)) + o.T).T)


def main():
    query_template("101_1.png")

# Main function calling
if __name__ == "__main__":
    main()

# def scoring_template(query_template, secured_template, threshold=3):
#     n = len(query_template)
#     m = len(secured_template)
#     match = [[False for i in range(m)] for j in range(n)]
#     for i in range(n):
#         q_x, q_y, q_z, = query_template[i]
#         for j in range(m):
#             s_x, s_y, s_z = secured_template[j]
#             match[i][j] = ((q_x - s_x)**2 + (q_y - s_y)**2 +
#                            (q_z - s_z)**2 - threshold**2) <= 0

#     match = np.array(match)
#     mqt = 0
#     for i in range(n):
#         mqt += any([x == True for x in match[i, :]])
#     mtq = 0
#     for i in range(m):
#         mtq += any([x == True for x in match[:, i]])
#     score = min(mqt / n, mtq / m) * 100
#     return score



# def match_template(query_template,secured_template):

# #     m_set,sing_points = get_points(query_image_path)
# #     query_image = cv2.imread(query_image_path,0)

# #     query_secured_template = get_secure_template(query,keyset,m_set,sing_points)
    
#     '''
#         11 iterations part needs to be implemented
#     '''
#     match_radius = 76
#     max_score = -float('inf')
#     for i in range(-5,6):
#         rotated_template = rotate_(query_template,i)
#         score = scoring_template(rotated_template,secured_template,match_radius)
#         if score > max_score:
#             max_score = score
#     return max_score