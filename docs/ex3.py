#!/usr/bin/bash
'''cloudprocesser-example.py | Implements main use case of cloudprocessor.'''

from cloudprocessor import *
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

##############################################################################
# TEST

clouds = [cloud1]
resolution = 1.
verbose = True

# Read an input xyz space-delimited point cloud to Cloud object.
c = Cloud(clouds)

# Merge the two, updating class extrema for x, y, z.
c.__merge__() 

# ------------------------------------------------------------------------

# Get Axis instances.
xax = Axis("x", res=resolution, min=c.xmin, max=c.xmax)
yax = Axis("y", res=resolution, min=c.ymin, max=c.ymax)
zax = Axis("z", res=resolution, min=c.zmin, max=c.zmax)

# Get function that indexes cloud over it's three axes for an input voxel.
Indexer = c.Index(xax, yax, zax)

# Get instance of class Grid.
g = Grid(xax, yax, zax)

# Index cloud over the three axes.
test = g.Statistic(Indexer)
print(test)

# # ------------------------------------------------------------------------
# if verbose: print("## Process cloud according to Axes instances.")

# # Get the indices for cells on each axis that contain points.
# if verbose: print(" - Indexing cloud over each axis.\n")
# ref_cloud       = CI.cloud.merged[["x", "y", "z"]].compute()
# ref_cloud["xi"] = CI.cloud.merged.x.apply(xax.__ix__) #.compute()
# ref_cloud["yi"] = CI.cloud.merged.y.apply(yax.__ix__) #.compute()
# ref_cloud["zi"] = CI.cloud.merged.z.apply(zax.__ix__) #.compute()
# CI.ref_cloud = ref_cloud
# print(CI.ref_cloud)

# # Get the unique indices for cells on each axis that contain points.
# if verbose: print(" - Finding unique indices for each axis.\n")
# mcxi_unq = np.sort(mcxi.unique().compute().tolist())
# mcyi_unq = np.sort(mcyi.unique().compute().tolist())
# mczi_unq = np.sort(mczi.unique().compute().tolist())

# # ------------------------------------------------------------------------
# if verbose: print("## Initialize Grid instance for Axes instances.")



# # Build indexer of the same shape as grid.ref_grid.
# if verbose: print(" - Build reference index for Grid instance.\n")
# CI.grid.__build__()

# # ------------------------------------------------------------------------
# if verbose: print("## Compute gridded stats for points mapped to Axes.")

# def PointsMean3D(xi, yi, zi):
#     indexed_points = CI.ref_cloud.loc[
#         (CI.ref_cloud.xi == xi) &
#         (CI.ref_cloud.yi == yi) &
#         (CI.ref_cloud.zi == zi) ]
#     return np.array([ indexed_points.x.mean(skipna=True), 
#                       indexed_points.y.mean(skipna=True), 
#                       indexed_points.z.mean(skipna=True) ])


# Test = []
# n = CI.grid.ref_index.shape[0]
# progressBar(0, n, pre='Progress:', suf='Complete', width=50)
# for i, v in enumerate(CI.grid.ref_index):
#     progressBar(i + 1, n, pre='Progress:', suf='Complete', width=50)
#     res = PointsMean3D(v[0], v[1], v[2])
#     Test.append(res)



#test = CI.grid.ref_index.apply(PointsMean3D)

#return(test)




#test = BuildCloudIndex([cloud1], resolution=1., verbose=True)
#print(test)