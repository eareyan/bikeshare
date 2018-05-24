#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 17:14:28 2018

@author: enriqueareyan
"""
import pulp as plp
import numpy as np
from util import check_integer_values, printSolution
import sys


def runExample1(tol):
    # We found an example where the LP optimal solution is not integral! 
    # 1 rider, 2 stations, and the following parameters.
    # In this counter example, a rider frees space and games the system!
    bikes = [1,1]
    empty = [0,1]
    valuations = [[[0, 1] , 
                   [2, 0]]]
    runBikeShareMatchingLP(bikes, empty, valuations, tol)

def runExample2(tol):
    bikes = [1, 1]
    empty = [1, 0]
    valuations = [[[0.83, 0.74],
                  [0, 0]],
                  [[0, 0.81],
                  [0.43, 0]]]
    runBikeShareMatchingLP(bikes, empty, valuations, tol, True)
    
def runRandomShareMatchingLP(num_riders, num_stations, tol):
    # Draw random valuations.
    valuations = [[[np.random.random() for s in range(0, num_stations)] for t in range(0, num_stations)] for i in range(0, num_riders)]
    # Draw random numbers for bikes and empty spaces.
    bikes = np.random.choice(50, num_stations)
    empty = np.random.choice(50, num_stations)
    return runBikeShareMatchingLP(bikes, empty, valuations, tol)

def runBikeShareMatchingLP(bikes, empty, valuations, tol, print_solution = False):
    # Get the number of stations and riders
    num_stations = len(bikes)
    num_riders = len(valuations)
    
    # Initialize LP
    prob = plp.LpProblem("Bike-Share Matching Problem", plp.LpMaximize)

    # Float variables x_ij \in [0,1]
    variables = [[[plp.LpVariable("x_" + str(i) + "_" + str(s) + "_" + str(t), lowBound = 0 , upBound = 1, cat = 'Integer') for t in range(0, num_stations)] for s in range(0, num_stations)] for i in range(0, num_riders)]
    #variables = [[[plp.LpVariable("x_" + str(i) + "_" + str(s) + "_" + str(t), lowBound = 0 , upBound = 1, cat = 'Continuous') for t in range(0, num_stations)] for s in range(0, num_stations)] for i in range(0, num_riders)]
    
    # Welfare-maximizing objective funciton
    prob += sum(valuations[i][s][t] * variables[i][s][t] for t in range(0, num_stations) for s in range(0, num_stations) for i in range(0, num_riders))
    
    # Each bidder is assigned at most one source-sink pair
    for i in range(0, num_riders):    
        prob += sum(variables[i][s][t] for t in range(0, num_stations) for s in range(0, num_stations)) <= 1.0
    
    # Each station s can only provide at most b_s bikes
    for k in range(0, num_riders):    
        range_bidders = [i for i in range(0, num_riders) if i != k]
        for s in range(0, num_stations):    
            for t in range(0, num_stations):   
                prob += variables[k][s][t] + sum(variables[i][s][t_prime] 
                for t_prime in range(0, num_stations) 
                for i in range_bidders) <= bikes[s]
                

    # Each station t can only receive at most e_s bikes plus the number of bikes leaving the station
    for k in range(0, num_riders):    
        range_bidders = [i for i in range(0, num_riders) if i != k]
        for s in range(0, num_stations):    
            for t in range(0, num_stations):   
                prob += variables[k][s][t] + sum(variables[i][s_prime][t] - variables[i][t][s_prime] 
                for s_prime in range(0, num_stations) 
                for i in range_bidders) <= empty[t]
    
    '''
    # Each station s can only provide at most b_s bikes
    for s in range(0, num_stations):    
        prob += sum(variables[i][s][t] for t in range(0, num_stations) for i in range(0, num_riders)) <= bikes[s]
    
    # Each station t can only receive at most e_s bikes plus the number of bikes leaving the station
    for t in range(0, num_stations):    
        prob += sum(variables[i][s][t] - variables[i][t][s] for s in range(0, num_stations) for i in range(0, num_riders)) <= empty[t] 
        
    # A constraint to avoid a user making space on its own
    for t in range(0, num_stations):
        prob += sum(variables[i][s][t] - variables[i][t][s] for s in range(0, num_stations) for i in range(0, num_riders)) <= empty[t]
                
    '''
    # Save model
    prob.writeLP("BikeShareMatching.lp")
    
    # Solve
    prob.solve()
    
    print("program value", plp.value(prob.objective))
    if(print_solution):
        printSolution(prob)
    
    return check_integer_values(plp, prob, tol)

# Run experiments with a very low tolerance. 
tol = 0.001
while(True):
    for riders in range(1, 5):
        for stations in range(1, 5):
            print("riders = " , riders , ", stations = ", stations)
            if not(runRandomShareMatchingLP(riders , stations, tol)):
                sys.exit("Found a counterexample")