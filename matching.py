#!/usr/bin/env python3

"""
This python script will implement following functionalities:
1) Perform one to one matching between query and a template stored in database. 
2) Perform one to many matching between query and templates stored in database.

Both of the function will return the matching score(highest matching score in case of one to many) which will be calculated as
    matching score = ((min(mns/ns, mnq/nq))*100)
"""

import cv2
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
[x] Calculate hausdroff distance between every point in query with stored template and vice versa and the point is matched if the hausdroff dis is less than a threshold(T1)
[x] Now rotate the query template from -60 to 60 degrees 1 degree at a time to remove rotation invariant.
[x-] Calculate matching score for each rotated query template and template stored in database. 
[x] Max out the matching score and compare it with the threshold(T2 or T) to know if the query and stored template is matched or not.
[x] Repeat this process for every stored template to get the exact result.
"""

# This function rotates the input set of points by a certain degrees
def rotate(p, origin=(0, 0), degrees=0):
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((np.dot(R, (p.T-o.T)) + o.T).T)

# This function takes two template as input and return the common point between two templates. The order of passing the template is important
def hausdroff_score(qtemplate, dtemplate, threshold):
    count = 0

    for i in range(len(qtemplate)):
        x = qtemplate[i][0]
        y = qtemplate[i][1]
        
        min_dist = np.inf
        for j in range(len(dtemplate)):
            dist = math.sqrt( (x-dtemplate[j][0])*(x-dtemplate[j][0]) + (y-dtemplate[j][1])*(y-dtemplate[j][1]) )

            if(min_dist > dist):
                min_dist = dist
        
        if(min_dist < threshold):
            count = count + 1
    
    return count

# This is a scoring function this takes two templates as a input and return the matching score
def matching_score(qtemplate, dtemplate, threshold1):
    n_q = len(qtemplate)
    n_s = len(dtemplate)
    mn_s = hausdroff_score(dtemplate, qtemplate, threshold1)
    mn_q = hausdroff_score(qtemplate, dtemplate, threshold1)

    score = min(mn_s/n_s, mn_q/n_q)*100

    return score

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
        save_file_name, modified_minutiae_list =  tp.generate_template(sx, sy, minutiae_list, s, p, q, r, file_name)
        modified_minutiae_list = np.array(modified_minutiae_list)

        # save_template(save_file_name, modified_minutiae_list)
        # with open(save_file_name, 'w') as fp:
        #     for item in modified_minutiae_list:
        #         x = item[0]
        #         y = item[1]
        #         s = "%s %s\n" % (x, y)
        #         fp.write(s)

    return modified_minutiae_list

# This function calculates the best template for a query template by rotating the query template and maximising the hausdroff scores of the template
def calculate_best_template(query_template,databse_template, threshold, origin):    
    # Rotate the image 1 degree at a time using s0*cos(r0), s0*sin(r0) as the center and calculate the hausdroff distance4
    alpha = 60
    best_template = query_template
    best_score = -np.inf
    for i in range(-1*alpha, alpha, 1):
        template = rotate(query_template, origin, i)
        h_score = hausdroff_score(template, databse_template, threshold)
        if(h_score > best_score):
            best_score = h_score
            best_template = template
    
    return best_template

def one_to_one_matching(qtemplate, dtemplate, threshold1, threshold2, origin):
    best_qtemplate = calculate_best_template(qtemplate, dtemplate, threshold1, origin)
    m_score = matching_score(best_qtemplate, dtemplate, threshold1)
    if(m_score >= threshold2):
        return "Matched"
    else:
        return "Not_Matched"

# This function performs one to many matching. The inputs are query_template and Directory containing all the templates. It returns the name of the template that are considered matched
def one_to_many_matching(qtemplate, template_database, threshold1, threshold2, origin):
    matched_template_path = []
    # Go thorugh all the stored database in the template database directory
    for path in os.listdir(template_database):
        final_path = os.path.join(template_database, path)
        if(os.path.isfile(final_path)):
            dtemplate = []
            with open(final_path) as f:
                lines = f.readlines()
                for line in lines:
                    temp = line.split()
                    x, y = float(temp[0]), float(temp[1])
                    dtemplate.append([x, y])
        
            dtemplate = np.array(dtemplate)
            best_qtemplate = calculate_best_template(qtemplate, dtemplate, threshold1, origin)
            m_score = matching_score(best_qtemplate, dtemplate, threshold1)
            print(m_score)
            if(m_score >= threshold2):
                matched_template_path.append(final_path)
    
    return matched_template_path

def main():
    p, q, r, s = tp.read_keyset()
    origin = (s*math.cos(math.radians(r)), s*math.sin(math.radians(r)))

    # Defining the values of threshold
    threshold1 = 5
    threshold2 = 50

    qtemplate = query_template("101_1.png")
    path = one_to_many_matching(qtemplate, "Templates", threshold1, threshold2, origin)

    print(path)


# Main function calling
if __name__ == "__main__":
    main()
