#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 12:59:05 2018

@author: enriqueareyan
"""

import pulp as plp
import numpy as np
import sys
from util import all_distinct, check_integer_values

""" 
    This function generates a random valuation v_ij, an solves
    the matching problem by solving an LP. It then checks that
    each decision variable x_ij is within a tolerance of either 0 or 1,
    thus empirically checking that the LP returns an integer solution.
"""
def runMatchingLP(n, m, tol):
    # a matrix with entry v_ij beign the value that bidder i has for item j
    valuations = [[np.random.random() for j in range(0, m)] for i in range(0, n)]
    if not(all_distinct(valuations)):
        print("There are repeat values in valuations")
        return False
        
    # Initialize LP
    prob = plp.LpProblem("Matching Problem", plp.LpMaximize)
    
    # Float variables x_ij \in [0,1]
    variables = [[plp.LpVariable("x_" + str(i) + "_" + str(j), lowBound = 0 , upBound = 1) for j in range(0, m)] for i in range(0, n)]
    
    # Welfare-maximizing objective funciton
    prob += sum(valuations[i][j] * variables[i][j] for j in range(0, m) for i in range(0, n))
    
    # Each bidder is assigned at most one item
    for i in range(0, n):    
        prob += sum(variables[i][j] for j in range(0, m)) <= 1.0
    
    # Each item is assigned to at most one bidder
    for j in range(0, m):    
        prob += sum(variables[i][j] for i in range(0, n)) <= 1.0
    
    # Save model
    prob.writeLP("Matching.lp")
    
    # Solve
    prob.solve()
    
    # Check solutions
    return check_integer_values(plp, prob, tol)

# Run experiments with a very low tolerance. 
tol = 0.00000000001
for n in range(1, 101):
    for m in range(1, 101):
        print("n = " , n , ", m = ", m)
        if not(runMatchingLP(n , m, tol)):
            sys.exit("Found a counterexample")     