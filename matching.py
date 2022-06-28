#!/usr/bin/env python3

"""
This python script will implement following functionalities:
1) Perform one to one matching between query and a template stored in database. 
2) Perform one to many matching between query and templates stored in database.

Both of the function will return the matching score(highest matching score in case of one to many) which will be calculated as
    matching score = ((min(mns/ns, mnq/nq))*100)
"""