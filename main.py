# -*- coding: utf-8 -*-
import numpy
import pygame

"""
GENETIC ALGORITHM OUTLINE 

 1: Randomly generate population
 2: Evaluate fitness of the population
     Repeat until required fitness score aquired
         Select N parent chromosomes to make next population
         Apply crossover (with probability)
         Apply mutation (with probability)
         Generate new population\
        
        
        Flappy bird has 3 potential inputs, bird position, top pipe position,
        bottom pipe position, and one output, jump.
        
        Therefore can assume one output neuron with 3 inputs, and use binary
        bits for the 'chromosome'. 
        
        3 inputs = 3 weights
        
"""

num_of_mating_parents = 4

population_size = 100

new_population = numpy.random.uniform(low=-1, high = 1, size=population_size)
print(new_population)

learning_rate = 0.01
