#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 18:03:35 2018

@author: enriqueareyan
"""

"""
    This function checks whether the given value is within a tolerance of 0 or 1.
    Returs true if that is the case, false othewise.
"""
def test_0_or_1(value, tol):
    if abs(value) <= tol or abs(value - 1) <= tol:
        return True
    else:
        return False

"""
    This function checks if all the entries of a matrix are distinct
"""
def all_distinct(M):
    for i in range(0, len(M)):
        for j in range(0, len(M[0])):
            for k in range(0, len(M)):
                for l in range(0, len(M[0])):
                    if(not(i==k and j==l) and M[i][j] == M[k][l]):
                        return False
    return True

"""
    Given a solution to the LP, check that all values are integer 0 or 1
    within the given tolerance
"""
def check_integer_values(plp, prob, tol):
    # The status of the solution is printed to the screen. 
    print("Status:", plp.LpStatus[prob.status])
    if plp.LpStatus[prob.status] != "Optimal":
        # The LP should be optimal. Return false otherwise.
        return False
    
    # Check that all the variables are 0 or 1.
    for v in prob.variables():
        if(not(test_0_or_1(v.varValue, tol))):
            for v in prob.variables():
                print(v.name, "=", v.varValue)
            print("PROBLEM!, we have found a fractional solution.")
            return False
    print("ALL GOOD!, total sum ", sum(x.varValue for x in prob.variables()))
    return True

"""
    Print values of solution
"""
def printSolution(prob):
    for v in prob.variables():
        print(v.name, "=", v.varValue)
    