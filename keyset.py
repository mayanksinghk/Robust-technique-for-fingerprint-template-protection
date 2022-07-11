#!/usr/bin/env python3
import numpy as np
import os


# This function returns the keyset values that is p0, q0, r0 and s0 given the lower limit and upper limit for key
def generate_keyset(llimit = 1, ulimit = 11, num = 1):
    keys = []
    # This key set is according to paper for diversity 
    for i in range(num):
        p = np.random.randint(llimit, ulimit)
        q = np.random.randint(llimit, ulimit)
        r = np.random.randint(llimit, ulimit)
        keys.append((p, q, r))
    
    return keys

def save_keyset(keys):
    filename = os.getcwd() + "/key.txt"
    print(filename)
    with open(filename, 'w') as fp:
        for item in keys:
            p = item[0]
            q = item[1]
            r = item[2]
            s = "%s %s %s\n" % (p, q, r)
            fp.write(s)

def main():
    keys = generate_keyset()
    print(keys)
    save_keyset(keys)

if __name__ == '__main__':
    main()
    