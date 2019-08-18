import numpy as np


def _permute_arrays(arrays):
    """Generate an array of voxel centroids from three dimensional arrays."""  
    arrays = [np.asarray(x) for x in arrays]  # Ensure all inputs are arrays.
    shape  = (len(x) for x in arrays)         # Get shape of each as a tuple.    
    ndims  = np.indices(shape)                # Get shape as array.
    index  = ndims.reshape(len(arrays), -1).T # Transpose.
    
    # Create empty 3d array, add axis positions, return.
    permuted = np.empty_like(index, dtype=arrays[0].dtype)
    for n, arr in enumerate(arrays):
        permuted[:, n] = arrays[n][index[:, n]]    
    return(permuted)


class Grid:
    """Initializes a grid for one or more axes."""
    size  = 1
    axes  = {}
    grid  = None
    index = None
    shape = []

    def __init__(self, *axes):    
        for ax in axes:                        # Iterate over input axes.
            self.__add__(ax)                   # Add to grid.
        self.__grid__()                        # Permute axes arrays.  
        self.__build__()                       # Permute axes indices.  

    def __add__(self, axis, grid: bool=False):
        """Add a new axis to the class."""
        setattr(self, axis.name, axis)         # Add axis to class attributes.
        self.axes[axis.name] = axis            # Add axis to reference dict.
        self.shape.append(axis.size)           # Append size to shape.
        if grid: self.__grid__()               # Permute axes if grid is True.

    def __grid__(self):
        """Wrapper for _permute_arrays."""
        ax = (ax.mid_points for ax in self.axes.values())
        self.grid = _permute_arrays(ax)        # Permute axis coordinates.
        self.size = self.grid.size             # Update total size of grid.

    def __build__(self):
        """ """
        ix = (range(ax.size) for ax in self.axes.values())
        self.index = _permute_arrays(ix).T     # Permute axis index.

    def Statistic(self, Indexer):
        """Builds indexer table of x, y, z indexes. Stats cols go here."""

        # Make a function that with xyz array as input and output.
        def calc(xyz):
            points = Indexer(xyz[0], xyz[1], xyz[2])
            result = np.array([  
                points.x.mean(skipna=True),
                points.y.mean(skipna=True),
                points.z.mean(skipna=True) ])
            return(result)

        # Vectorize the function.
        vfunc = np.vectorize(calc)

        result = vfunc(self.index.T)

        return(result)










    #def __stat__(self, cloud):
    #    """ """
    #    idx = (range(ax.size) for ax in self.axes.values())
    #    self.index = _permute_arrays(idx)  # Permute axis index.


