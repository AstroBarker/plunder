#!/usr/bin/env python3

# -----------------------------------------------------------------------------
#
#  -------------------------
#  Author: Brandon Barker
#  -------------------------
# 
#  Randomly select ...
#
# -----------------------------------------------------------------------------

import numpy as np

f = 3.0 / 4.0 # Ratio between probability weights

def tier_sizes(tiers):
    """
    Return number of people in each tier
    """

    # Finds number of times unique elements of tiers appear ([1] gets rid of unnecessary output)
    n = np.unique(tiers, return_counts=True)[1]

    return n

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

if __name__ == '__main__':
    # yee haw
    print('\n**********************************************************')
    print( '**** ROSSINI: RandOmized diScuSsIoN group leader selectIon')
    print( '***********************************************************\n') 
    fn = 'test_people.dat'

    people, tiers = np.genfromtxt(fn, skip_header=1, unpack=True, dtype='unicode')

    tiers, people = sortt(tiers, people)
    
    n = tier_sizes(tiers)
    
    w = weights(f,n)

    winner = np.random.choice(people, 1, p=w)[0]

    print(f'The participants and their respective weights are: \n {list(zip(people,w))}\n\n')
    print(f'Just to check... the weights, summed, should equal... {sum(w)}\n')
    print('\n---------------------------------------------------- ')
    print(f'The next discussion group leader is {winner}!!!!!')
    print('---------------------------------------------------- \n')