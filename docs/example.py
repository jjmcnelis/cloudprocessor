#!/usr/bin/bash
'''cloudprocesser-example.py | Implements main use case of cloudprocessor.'''

import cloudprocessor as cp
import numpy as np
import warnings
import sys

warnings.filterwarnings("ignore")
print("-"*62)

try:
    TEST, cloud1, cloud2 = sys.argv
    print("\nINFO: Processing input clouds - %s, %s." % (cloud1, cloud2))   
except:
    TEST, cloud1, cloud2 = "SCRIPT","tests/tls1.xyz","tests/tls2.xyz"
    print("\nWARN: Arguments invalid or not provided. Using test files.")

### CLOUD --------------------------------------------------------------------

# Read an input xyz space-delimited point cloud to Cloud object.
print("INFO: Testing instantiation of class Cloud.")
myCloud = cp.Cloud(["tests/tls1.xyz"])
# Add a second cloud. This will not merge it with base cloud.
print("INFO: Testing Cloud.__add__(<cloud.xyz>).")
myCloud.__add__("tests/tls2.xyz")
# Merge the two.
print("INFO: Testing Cloud.__merge__().\n")
myCloud.__merge__() 

### AXIS ---------------------------------------------------------------------
print("-"*62)

# Get the min and max of myCloud.
print("INFO: Computing min and max of each axis of cloud: x, y, z.\n")
mcx = myCloud.merged.x.min().compute(), myCloud.merged.x.max().compute()
print(" - x:\t\t\t%s, %s" % mcx)
mcy = myCloud.merged.y.min().compute(), myCloud.merged.y.max().compute()
print(" - y:\t\t\t%s, %s" % mcy)
mcz = myCloud.merged.z.min().compute(), myCloud.merged.z.max().compute() 
print(" - z:\t\t\t%s, %s\n" % mcz)

print("-"*62)

# Get axes.
print("INFO: Test instantiation of class Axis for each cloud axis.\n")
xax = cp.Axis("x", res=1, min=mcx[0], max=mcx[1])
print(" - x size:\t\t%s" % xax.size)
yax = cp.Axis("y", res=1, min=mcy[0], max=mcy[1])
print(" - y size:\t\t%s" % yax.size)
zax = cp.Axis("z", res=1, min=mcz[0], max=mcz[1])
print(" - z size:\t\t%s\n" % zax.size)

### GRID ---------------------------------------------------------------------
print("-"*62)

# Get a 1d grid.
print("\nINFO: Testing instantiation of class Grid with axis x.")
grid = cp.Grid(xax)
print(" - Grid shape:\t\t%s" % str(grid.ref_shape))

# Add another axis.
print("\nINFO: Testing Grid.__add__(< y axis >) with axis y.")
grid.__add__(yax, grid=True)
print(" - New shape:\t\t%s" % str(grid.ref_shape))

# Add a third axis.
print("\nINFO: Testing Grid.__add__(< z axis >) again with axis z.")
grid.__add__(zax, grid=True)
print(" - New shape:\t\t%s" % str(grid.ref_shape))

# Transpose to three long arrays.
print("\nINFO: Transposing the 3d grid of permuted axis.\n")
grid.ref_grid = grid.ref_grid.T

# Build indexer of the same shape as grid.ref_grid.
print("\nINFO: Testing Grid.__build__() to build indexer (same shape).\n")
grid.ref_index = grid.__build__()

##############################################################################
### INDEXING
##############################################################################
print("-"*62)

# Get the first cloud.
mc1 = myCloud.clouds["tests/tls1.xyz"]

# Get the unique indices for cells on each axis that contain points.
print("INFO: Testing cell indexing over each axis.\n")
mc1xb = mc1.x.apply(xax.__ix__)
mc1xb_unq = np.sort(mc1xb.unique().compute().tolist())
print(" - x axis unique: \t%s" % str(mc1xb_unq))
mc1yb = mc1.y.apply(yax.__ix__)
mc1yb_unq = np.sort(mc1yb.unique().compute().tolist())
print(" - y axis unique: \t%s" % str(mc1yb_unq))
mc1zb = mc1.z.apply(zax.__ix__) 
mc1zb_unq = np.sort(mc1zb.unique().compute().tolist())
print(" - z axis unique: \t%s" % str(mc1zb_unq))

