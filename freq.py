# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:24:18 2016

@author: jweissman
"""

from __future__ import print_function

import argparse
from gooey import Gooey, GooeyParser

###########################################

import networkx as nx
#import scipy as sp
#import re
 
import numpy as np
import pandas as pd
import sqlite3 as sql
import csv
#import glob
#import os
#import matplotlib.pyplot as plt
from pylab import *


# dict defining abbreviations for populations
populations = {
  'war' : 'Warren',
  'cat' : 'Cathedral',
  'gib' : 'Gibbs',
  'con' : 'Convict',
  'whe' : 'Wheeler',
  'tab' : 'Taboose',
  'saw' : 'Sawmill',
  'bax' : 'Baxter',
  'bub' : 'Bubbs',
  'wil' : 'Williamson',
  'lan' : 'Langley',
  'ola' : 'Olancha',
  'bar' : 'Big Arroyo',
  'lau' : 'Laurel',
  'cdd' : 'Casa Diablo Deer',
  'rvd' : 'Round Valley Deer',
  'gde' : 'Goodale Deer',
  'pro' : 'Pronghorn',
  'bbo' : 'Butermilks Bobcat', 
  'bpb' : 'Big Pine Bobcat',
  'ibo' : 'Independence Bobcat',
  'lpb' : 'Lone Pine Bobcat',
  'obo' : 'Olancha Bobcat',
  'cme' : 'Crater Mountain Elk',
  'iel' : 'Independence Elk',
  'lpe' : 'Lone Pine Elk',
}

populations_df = pd.DataFrame({'location': 
  {0: 'CDB',
 1: 'Olancha Peak',
 2: 'RVD',
 3: 'Bodie Hills',
 4: 'Mt. Williamson',
 5: 'GD0',
 6: 'Taboose Creek',
 7: 'Sawmill Canyon',
 8: 'Round Valley',
 9: 'Mt. Gibbs',
 10: 'Mt. Warren',
 11: 'Independence Elk',
 12: 'Wheeler Ridge',
 13: 'Mt. Langley',
 14: 'Bubbs Creek',
 15: 'Laurel Creek',
 16: 'Olancha Bobcat',
 17: 'Big Pine Bobcat',
 18: 'Big Arroyo',
 19: 'Independence Bobcat',
 20: 'Crater Mountain Elk',
 21: 'Mt. Baxter',
 22: 'Cathedral',
 23: 'Lone Pine Elk',
 24: 'Bobcat',
 25: 'Convict Creek'},
 'species': {0: 'deer',
 1: 'bighorn',
 2: 'deer',
 3: 'Pronghorn',
 4: 'bighorn',
 5: 'deer',
 6: 'bighorn',
 7: 'bighorn',
 8: 'Bobcat',
 9: 'bighorn',
 10: 'bighorn',
 11: 'Elk',
 12: 'bighorn',
 13: 'bighorn',
 14: 'bighorn',
 15: 'bighorn',
 16: 'Bobcat',
 17: 'Bobcat',
 18: 'bighorn',
 19: 'Bobcat',
 20: 'Elk',
 21: 'bighorn',
 22: 'bighorn',
 23: 'Elk',
 24: 'Bobcat',
 25: 'bighorn'},
 'label': {0: 'cdd',
 1: 'ola',
 2: 'rvd',
 3: 'pro',
 4: 'wil',
 5: 'gde',
 6: 'tab',
 7: 'saw',
 8: 'bbo',
 9: 'gib',
 10: 'war',
 11: 'iel',
 12: 'whe',
 13: 'lan',
 14: 'bub',
 15: 'lau',
 16: 'obo',
 17: 'bpb',
 18: 'bar',
 19: 'ibo',
 20: 'cme',
 21: 'bax',
 22: 'cat',
 23: 'lpe',
 24: 'lpb',
 25: 'con'}}
)



popSpeciesLocationDict = {
  'war' : 'bighorn@Mt. Warren',
  'cat' : 'bighorn@Cathedral',
  'gib' : 'bighorn@Mt. Gibbs',
  'con' : 'bighorn@Convict Creek',
  'whe' : 'bighorn@Wheeler Ridge',
  'tab' : 'bighorn@Taboose Creek',
  'saw' : 'bighorn@Sawmill Canyon',
  'bax' : 'bighorn@Mt. Baxter',
  'bub' : 'bighorn@Bubbs Creek',
  'wil' : 'bighorn@Mt. Williamson',
  'lan' : 'bighorn@Mt. Langley',
  'ola' : 'bighorn@Olancha Peak',
  'bar' : 'bighorn@Big Arroyo',
  'lau' : 'bighorn@Laurel Creek',
  'cdd' : 'deer@CDB',
  'rvd' : 'deer@RVD',
  'gde' : 'deer@GD0',
  'pro' : 'Pronghorn@Bodie Hills',
  'bbo' : 'Bobcat@Round Valley', 
  'bpb' : 'Big Pine Bobcat',
  'ibo' : 'Independence Bobcat',
  'lpb' : 'Bobcat',
  'cme' : 'Crater Mountain Elk',
  'iel' : 'Independence Elk',
  'lpe' : 'Lone Pine Elk',
}



# these are normalized centerpoints for sheep herds
# they are computed from homerange shapefiles
herdLayout = {'bar' : [ 0.13426307, -0.53816364], 
              'bub' : [ 0.13508144, -0.22975496],  
              'bax' : [ 0.31588085, -0.18501160], 
              'cat' : [-0.89312635,  0.73123947], 
              'con' : [-0.23264139,  0.50181201], 
              'gib' : [-0.72999145,  0.83111162], 
              'lan' : [ 0.46999905, -0.51692227],  
              'lau' : [ 0.20128761, -0.69087122],  
              'ola' : [ 0.60590522, -0.77055854],  
              'saw' : [ 0.28474177, -0.11160737],  
              'tab' : [ 0.24773331, -0.02421425], 
              'whe' : [-0.11685254,  0.38189278],  
              'wil' : [ 0.37293368, -0.37846646], 
              'war' : [-0.79521428,  0.99951444]}

allCollarsFieldNames = ['frequency',
                        'capture_date',
                        'species',
                        'animal_id',
                        'region',
                        'type',
                        'make',
                        'status',
                        'location']


# array comparison function
# this is a more efficient, less straightforward solution
# see https://github.com/numpy/numpy/issues/7784
def in1d_tolerance(a, b, tol=1e-6):
    a = np.unique(a)
    intervals = np.empty(2*a.size, float)
    intervals[::2] = a - tol
    intervals[1::2] = a + tol
    overlaps = intervals[:-1] >= intervals[1:]
    overlaps[1:] = overlaps[1:] | overlaps[:-1]  
    keep = np.concatenate((~overlaps, [True]))
    intervals = intervals[keep]
    return np.searchsorted(intervals, b, side='right') & 1 == 1
    
# unused_values
# find values in all_values that are more than tol away from
# any value in used_values
def unused_values(all_values, used_values, tol=0.005):
  return [x for x in all_values if all(np.abs( used_values - x) > 0.005) ]
       

#collars = pd.read_csv('AllCollarsList.txt', header=None, names=allCollarsFieldNames)
collars = pd.read_csv('AllCollarsList.txt')
active_collar_locations = collars[collars.status.str.match(r'^AW', as_indexer=True)]['location'].unique()
active_populations =  (collars[collars.status.str.match(r'^AW', as_indexer=True)]['species'] + 
                      ' | ' + 
                      collars[collars.status.str.match(r'^AW', as_indexer=True)]['location']).unique()
    
ALL_FREQUENCIES = np.r_[159.0:161.0:0.001]


network_file = "adjacencylist.txt"
popGraphFile = open(network_file, "r")
popGraph = nx.read_adjlist(popGraphFile)

# unused_frequencies = [x for x in ALL_FREQUENCIES if all(np.abs( freqs - x ) > 0.005) ]


###########################################

def bandwidthComplement(all_freqs, input_freqs, freq_width = 0.01) : 
  freq_margin = freq_width/2
  complement_freqs = [x for x in all_freqs if all(np.abs( input_freqs - x) > freq_margin)]
  return(complement_freqs)

def findAvailablePops(input_frequency, input_species = 'none') :
  nearby_collars = collars[(collars.status.str.match(r'^AW')) & 
    (np.abs(collars.frequency - input_frequency) < 0.005) ]
  occupied_locations = nearby_collars['location'].unique()
  occupied_pops = populations_df[populations_df.location.isin(occupied_locations)]['label'].unique()
  invalid_pops = list(occupied_pops)
  for pop in occupied_pops: 
    invalid_pops += popGraph.neighbors(pop)
  invalid_pops = unique(invalid_pops)
  valid_pops = populations_df[populations_df.label.isin(invalid_pops) == False]
  if input_species != 'none':
    valid_pops = valid_pops[valid_pops.species == input_species]
  return(valid_pops)


def findAvailableFreqs(input_pops, all_freqs = ALL_FREQUENCIES) : 
  neighborhood_pops = []
  for pop in input_pops :
    neighborhood_pops += popGraph.neighbors(pop) + [pop]
  neighborhood_pops = np.unique(neighborhood_pops)
  neighborhood_freqs = np.array([])
  for pop in neighborhood_pops : 
    spec = populations_df[populations_df.label == pop]['species'].iloc[0]
    loc  = populations_df[populations_df.label == pop]['location'].iloc[0]
    used = collars[ (collars.species == spec) & (collars.location == loc) ]['frequency'].values
    neighborhood_freqs = append(neighborhood_freqs, used)
  neighborhood_freqs.sort()
  neighborhood_freqs = np.unique(neighborhood_freqs) 
  return bandwidthComplement(all_freqs, neighborhood_freqs)

def printFreqs(freq_list) :
  for f in freq_list : 
     print( "%3.3f" % (f) )
  
    
    
    
###########################################
#from message import display_message

running = True

@Gooey(program_name="Frequency Finder",
       optional_cols=2)

def main():
  desc = "VHF Collar Frequency Availability" 
  parser = GooeyParser(description = desc)
  parser.add_argument('--verbose', help='be verbose', dest='verbose',
                      action='store_true', default=False)
  
  subs = parser.add_subparsers(help='commands', dest='command')
 
  # Pop finder:
  popfinder_parser = subs.add_parser('popfinder', help='Input a frequency, find populations where it could be placed')
  popfinder_parser.add_argument('frequency', 
                                help='Enter a VHF frequency in KHz to find where it could be placed',
                                type=float)
  popfinder_parser.add_argument('species', help='Desired species',
                                choices=populations_df['species'].unique().tolist())                                

  # Frequency finder: 
  freqfinder_parser = subs.add_parser('freqfinder', help='Input populations, find frequencies that are available')
  freqfinder_parser.add_argument('population',
                                 choices=(populations_df.species + " @ " + populations_df.location).tolist(),
                                 help='pop input')
  

  
  
  args = parser.parse_args()
  
  if args.command == 'popfinder' :
    f = args.frequency
    print()
    print(f, " may be placed in these populations: ")
    print(findAvailablePops(input_frequency=f, input_species=args.species))
  elif args.command == 'freqfinder' :
    pop_str = args.population
    [species, location] = pop_str.split(' @ ')
    selected_pops_df= populations_df[ (populations_df.location == location) & 
                                      (populations_df.species == species)]
    pop_labels = selected_pops_df['label'].tolist()
    available_freqs = findAvailableFreqs(pop_labels)
    print()
    printFreqs(available_freqs)
    hist(available_freqs,bins=ALL_FREQUENCIES)
    
#  #display_message()
  
if __name__ == '__main__':
  main()