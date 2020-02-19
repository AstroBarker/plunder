#!/usr/bin/env python3

# -----------------------------------------------------------------------------
#
#  -------------------------
#  Author: Brandon Barker
#  -------------------------
# 
#  Randomly select a person from an input file with a "tiered, semi-uniform"
#  distribution. 
#
# -----------------------------------------------------------------------------

import numpy as np

f = 3.0 / 4.0 # Ratio between probability weights
REMOVE_PREV = True # Remove the previous leader from the current distribution?

def tier_sizes(tiers):
    """
    Return number of people in each tier
    """

    # Finds number of times unique elements of tiers appear ([1] gets rid of unnecessary output)
    n = np.unique(tiers, return_counts=True)[1]

    return n

def get_tier(name, people, tiers):
    """
    Return the tier of a specific person

    Parameters:
    -----------
    name : str, person whose tier is being looked up
    people : array, list of people
    tiers : array, list of tiers
    """

    ind = np.where(people == name)[0]    

    return tiers[ind]

def weights(f, n):
    """
    Return weights for my probability distribution,

    Parameters:
    -----------
    f : float, ratio of weights for different tiers
    n : array, contains the number of entries for each tier
    """
    N = np.max(n)
    v = np.zeros(len(n))

    # w[-1] = 1.0 / ( sum() )
    for i in range( len(n) ):
        v[-1] += f**(N-i) * n[i]
    v[-1] = 1.0 / v[-1]

    for i in range( len(n) ):
        v[i] = f**(N-i) * v[-1]
    
    # Now we've calculated all the weights, we load them into an array 
    # with n[0] copies of w[0], etc, such that we have one weight per person

    # Perhaps not the most efficient way....
    w = []
    for i in range(len(n)):
        w.append( np.ones(n[i])*v[i] )
    
    # w is a lis tof arrays. This concatenates it into a single array.
    w = np.concatenate(w, axis=None)

    return w


def sortt(a, b):
    """
    Sort lists  - a and b - consistently according to a
    Specifically, sorts the people array according to the tiers array, such that 
    all people of the same tier are together. This is necessary later for pairing with 
    the probability weights.

    Parameters:
    -----------
    a : array, tiers array. 
    b : array, people array.
    """
    zipped = sorted(zip(a,b))
    a,b = map(list, zip(*zipped)) 
    
    return a,b

def store_person(name, fn):
    """
    Write a name to a file for later use. 

    Parameters:
    -----------
    name : str, person
    fn : str, file to write to
    """

    with open(fn,"a") as file:
        file.write(name + '\n')
    
def get_previous_person(fn):
    """
    Get the last person to lead a discussion from the 
    file written in store_person()

    Parameters:
    -----------
    fn : str, filename to read
    """
    from os import path

    # This will trigger if fn doesn't exist, i.e., no one has pressented yet
    if not path.exists(fn): 
        return None
    else:
        ppl = np.genfromtxt(fn, skip_header=0, unpack=True, dtype='unicode')
        # Unnecessarily complicated.... if only one person was in the file, 
        # ppl isn't returned as an array from genfromtxt. So we just return ppl. 
        if ( np.shape(ppl) == () ):
            return ppl
        else:
            return ppl[-1]

def remove_person(people, tiers, prev):
    """
    Removes the last leader from the people, tiers arrays prior to 
    computing the weights and selecting a winner. This should not affect the 
    distribution, and is simply to allow for no repetitions.

    Parameters:
    -----------
    people : array
    tiers : array
    prev : str, person to have their entires remove from people, tiers.
    """

    ind = np.where(people == prev)[0]

    people = np.delete(people, ind)
    tiers = np.delete(tiers, ind)

    return people, tiers

if __name__ == '__main__':
    # yee haw
    print('\n**********************************************************')
    print( '**** ROSSINI: RandOmized diScuSsIoN group leader selectIon')
    print( '***********************************************************\n') 

    fn = 'test_people.dat'
    fn_out = 'people_old.dat'

    # Read in people, tiers, and check for previous leaders
    people, tiers = np.genfromtxt(fn, skip_header=1, unpack=True, dtype='unicode')
    prev = get_previous_person(fn_out)

    # If there was a previous leader AND you want to remove them, do so
    if ( prev != None and REMOVE_PREV == True):
        people, tiers = remove_person(people, tiers, prev)

    # Sort people according to their tiers
    tiers, people = sortt(tiers, people)

    # Number of tiers
    n = tier_sizes(tiers)
    
    # Probabalistic weights
    w = weights(f,n)

    #-----------------------------------------------------------
    #  We use numpy's random.choice function that will draw 
    #  random samples from a given population (people)
    #  with given probabilities (weights, w).
    #-----------------------------------------------------------
    winner = np.random.choice(people, 1, p=w)[0]
    
    # Keep track of leaders in fn_out. 
    # Future work: reduce their probabilities. Maybe lower their tiers?
    store_person(winner, fn_out)

    print(f'The participants and their respective weights are: \n {list(zip(people,w))}\n\n')
    print(f'Just to check... the weights, summed, should equal... {sum(w)} :)\n')
    print('\n---------------------------------------------------- ')
    print(f'The next discussion group leader is {winner}!!!!!')
    print('---------------------------------------------------- \n')
    # print(get_tier(winner, people, tiers))