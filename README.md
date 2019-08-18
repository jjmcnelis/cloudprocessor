# cloudprocessor

Simple, flexible, parallelized functions and classes for transforming and 
computing gridded statistics over point clouds. Built on NumPy and Dask.

- An instance of class `Axis` is defined by the min and max of the input 
  cloud(s) and the desired resolution(s) along the axis. 
  - an `Axis` has resolution (float) greater than zero.
  - an `Axis` can be scaled, rotated, translated (soon).
- An instance of class `Grid` is made of one or more instances of class `Axis`.
  - a `Grid` can (in theory) have any number of axes.
  - a `Grid`'s axes can have different resolutions.
- An instance of class `Cloud` is made of one or more point clouds.
  - Several file formats are supported + data can be imported straight from
    dask dataframes or arrays (soon).
  - All cloud operations are reduced to their equivalent over the cloud(s) 
    independent axes, so any number of operations can be applied to each.

author: jack mcnelis   |   email:  jjmcnelis@outlook.com
