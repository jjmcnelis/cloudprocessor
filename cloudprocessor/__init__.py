'''cloudprocessor

Simple, flexible, parallelized functions and classes for transforming and 
computing gridded statistics over point clouds. Built on NumPy and Dask.

- An instance of class Axis is defined by the min and max of the input 
  cloud(s) and the desired resolution(s) along the axis. 
  - an Axis has resolution (float) greater than zero.
  - an Axis can be scaled, rotated, translated (soon).
- An instance of class Grid is made of one or more instances of class Axis.
  - a Grid can (in theory) have any number of axes.
  - a Grid's axes can be any number of different resolution.
- An instance of class Cloud is made of one or more point clouds.
  - Several file formats are supported + data can be imported straight from
    dask dataframes or arrays (soon).
  - All cloud operations are reduced to their equivalent over the cloud(s) 
    independent axes, so any number of operations can be applied to each.

author: jack mcnelis
email:  jjmcnelis@outlook.com
'''

import numpy as np
import decimal

from .axis import Axis
from .cloud import Cloud
from .grid import Grid


# disallow scientific notation when printing
np.set_printoptions(suppress=True)


# Function to get the precision of user inputs.
def _get_precision(x: float):
    return abs(decimal.Decimal(str(x)).as_tuple().exponent)


# Print iterations progress
def progressBar(i, n, pre='', suf='', dec=1, width=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(dec) + "f}").format(100 * (i / float(n)))
    filledLength = int(width * i // n)
    bar = fill * filledLength + '-' * (width - filledLength)
    print('\r%s |%s| %s%% %s' % (pre, bar, percent, suf), end = '\r')
    # Print New Line on Complete
    if i == n: 
        print()


# ----------------------------------------------------------------------------
# EXAMPLE IMPLEMENTATION
# ----------------------------------------------------------------------------

class CloudIndex:
    """ """
    fclouds   = None
    nclouds   = None
    ref_cloud = None
    cloud     = None
    axes      = None
    grid      = None