#!/usr/bin/env python3

# -----------------------------------------------------------------------------
#
#  -------------------------
#  Author: Brandon Barker
#  -------------------------
#
#  Plot the distribution from rossini.py. Mostly just to check it out,
#  make sure it makes sense.
#
# -----------------------------------------------------------------------------

import rossini

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


def plot_bar_from_counter(counter, num, ax=None):
  """ "
  This function creates a bar plot from a counter.

  Parameters:
  -----------

  counter: This is a counter object, a dictionary with the item as the key
      and the frequency as the value
  ax: an axis of matplotlib
  num: number of samples, for normalization

  return: the axis with the object in it
  """

  if ax is None:
    fig = plt.figure()
    ax = fig.add_subplot(111)

  frequencies = counter.values()
  names = list(counter.keys())

  frequencies, names = rossini.sortt(frequencies, names)

  for i in range(len(frequencies)):
    frequencies[i] /= num

  x_coordinates = np.arange(len(counter))
  ax.bar(x_coordinates, frequencies, align="center", color="orchid")

  ax.xaxis.set_major_locator(plt.FixedLocator(x_coordinates))
  ax.xaxis.set_major_formatter(plt.FixedFormatter(names))
  ax.set(xlabel="Person", ylabel="Count")

  return ax


if __name__ == "__main__":
  fn = "people.dat"
  fn_out = "people_old.dat"

  num = 1000
  samples = np.array([rossini.draw_sample(fn, fn_out) for _ in range(num)])

  counts = Counter(samples)

  plot_bar_from_counter(counts, num)
  plt.show()
