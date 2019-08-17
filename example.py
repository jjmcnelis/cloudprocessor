#!/usr/bin/bash
'''cloudprocesser-example.py | Implements main use case of cloudprocessor.'''

import cloudprocessor as cp
import sys

t_ = "CHECK_ARGS","tests/tls1.xyz","tests/tls2.xyz"

try:
    TEST, cloud1, cloud2 = sys.argv
except:
    TEST, cloud1, cloud2 = t_
print(TEST)

# Read an input xyz space-delimited point cloud to Cloud object.
myCloud = cp.Cloud(["tests/tls1.xyz"])

# Add a second cloud. This will not merge it with base cloud.
myCloud.__add__("tests/tls2.xyz")

# Merge the two.
myCloud.__merge__() 

# Get the min and max of myCloud.
mcx = myCloud.merged.x.min().compute(), myCloud.merged.x.max().compute()
mcy = myCloud.merged.y.min().compute(), myCloud.merged.y.max().compute()
mcz = myCloud.merged.z.min().compute(), myCloud.merged.z.max().compute() 

# Get axes.
xax = cp.Axis("x", res=1, min=mcx[0], max=mcx[1])
yax = cp.Axis("y", res=1, min=mcy[0], max=mcy[1])
zax = cp.Axis("z", res=1, min=mcz[0], max=mcz[1])

# Get a 1d grid.
grid = cp.Grid(xax)
# Add another axis.
grid.__add__(yax, grid=True)
# Add a third axis.
grid.__add__(zax, grid=True)

# Transpose to three long arrays.
grid = grid.grid.T

# Get the first cloud.                 << this probably isnt right. snoozed.
mc1 = myCloud.clouds["tests/tls1.xyz"]
mc1xb = mc1.x.apply(xax.__ix__)
mc1yb = mc1.y.apply(xax.__ix__)
mc1zb = mc1.z.apply(xax.__ix__) 

### TEST -----------------------------------------------------------------

#print(myCloud.merged)
#print(mcx)
#print(mcy)
#print(mcz)
#print(xax)
#print(yax)
#print(zax)
#print(grid)
#print(grid.grid)
#print(mc1xb)
#print(mc1yb)
#print(mc1zb)