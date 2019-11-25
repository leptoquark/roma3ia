# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 15:29:38 2017

@author: Claudio Biancalana
"""
import random
import numpy
import math

TEMPERATURA_INIZIALE = 30
TEMPERATURA_FINALE = 0.2
ALFA = 0.99
STEPS_PER_CHANGE = 100

DIMENSIONE = 8

def tweak(sol):
    sol_copy = numpy.copy(sol)
    x = random.randint(0,DIMENSIONE-1)
    y = random.randint(0,DIMENSIONE-1)
    while x==y:
        y = random.randint(0,DIMENSIONE-1)
    temp = sol_copy[y]
    sol_copy[y] = sol_copy[x] 
    sol_copy[x] = temp
    return sol_copy

def inizializza(sol):
    for c in range(0,DIMENSIONE-1):
        tweak(sol)
    return tweak(sol)

def energia(matrix):
    board  = [[0] * DIMENSIONE for i in range(DIMENSIONE)] 
    for i in range(0,DIMENSIONE):
        board[i][matrix[i]]='Q'
        
    dx = [-1,1,-1,1]
    dy = [-1,1,1,-1]
    
    conflitti = 0

    for i in range(0,DIMENSIONE):
        x=i
        y=matrix[i]
        for j in range(0,4):
            tempx = x
            tempy = y
            while (True):
                tempx = tempx + dx[j]
                tempy = tempy + dy[j]
                if ((tempx < 0) or 
                    (tempx >= DIMENSIONE) or
                    (tempy < 0) or 
                    (tempy >= DIMENSIONE)):
                    break
                if (board[tempx][tempy]=='Q'):
                    conflitti = conflitti+1
    return conflitti

def stampa(sol):
    board = [[0] * DIMENSIONE for i in range(DIMENSIONE)] 
    for x in range(0,DIMENSIONE):
        board[x][sol[x]]='Q'
    print("SCHACCHIERA")
    for y in range(0,DIMENSIONE):
        for x in range(0,DIMENSIONE):
            if(board[x][y]=='Q'):
                print("Q"),
            else:
                print("."),
        print("\n")
    print("\n\n")

current = range(0,DIMENSIONE)
working = range(0,DIMENSIONE)
best = range (0,DIMENSIONE)

current = inizializza(current)
current_energy = energia(current)

best_energy = DIMENSIONE*(DIMENSIONE-1)

working = numpy.copy(current)
working_energy = current_energy

temperature = TEMPERATURA_INIZIALE

while (temperature > TEMPERATURA_FINALE and best_energy!=0):
    print("TEMPERATURA: "),    
    print(temperature)
    for step in range(0,STEPS_PER_CHANGE):
        useNew = False
        working = tweak(working)
        working_energy = energia(working)
    
        if (working_energy < current_energy):
            useNew = True
        else:
            test = random.random()
            delta = working_energy - current_energy
            calc = math.exp(-delta/temperature)
            if (calc > test):
                useNew = True
                
        if (useNew):
            current = numpy.copy(working)
            current_energy = working_energy
            
            if (current_energy < best_energy):
                best = numpy.copy(working)
                best_energy = energia(best)
            useNew = False
        else:
            working = numpy.copy(current)
            working_energy = energia(working)
            
    print("best_energy="),
    print(best_energy)            
    temperature = temperature * ALFA

stampa(best)
