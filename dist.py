#!/usr/bin/env python3

# -----------------------------------------------------------------------------
#
#  -------------------------
#  Author: Brandon Barker
#  -------------------------
# 
#  Plot the distribution from rossini.py
#
# -----------------------------------------------------------------------------

def plot_bar_from_counter(counter, ax=None):
    """"
    This function creates a bar plot from a counter.

    :param counter: This is a counter object, a dictionary with the item as the key
     and the frequency as the value
    :param ax: an axis of matplotlib
    :return: the axis wit the object in it
    """

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    frequencies = (counter.values())
    names = list(counter.keys())

    x_coordinates = np.arange(len(counter))
    ax.bar(x_coordinates, frequencies, align='center')

    ax.xaxis.set_major_locator(plt.FixedLocator(x_coordinates))
    ax.xaxis.set_major_formatter(plt.FixedFormatter(names))
    ax.set(xlabel = "Person", ylabel = "Count")

    return ax

if __name__ == '__main__':

    from rossini import *
    import matplotlib.pyplot as plt
    import pandas
    from collections import Counter

    fn = 'test_people.dat'

    people, tiers = np.genfromtxt(fn, skip_header=1, unpack=True, dtype='unicode')

    tiers, people = sortt(tiers, people)
    
    n = tier_sizes(tiers)
    
    w = weights(f,n)

    num = len(people) * 100
    samples = np.random.choice(people, num, p=w)

    counts = Counter(samples)

    plot_bar_from_counter(counts)
    plt.show()