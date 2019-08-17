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
    ref   = {}
    shape = []
    size  = 1
   
    def __init__(self, *axes):    
        for ax in axes:                        # Initialize input axes.
            self.__add__(ax)
        self.__grid__()                        # Permute axes arrays.  
        #self.x, self.y, self.z = x, y, z      # Initialize input axes.
        #self.size  = x.size*y.size*z.size     # Get total size of grid. 
        #self.shape = (x.size, y.size, z.size) # Get shape of grid.

    def __add__(self, axis, grid: bool=False):
        """Add a new axis to the class."""
        setattr(self, axis.name, axis)         # Get total size of grid. 
        self.ref[axis.name] = axis             # Get total size of grid.    
        if grid:
            self.__grid__()                    # Permute axes arrays. 

    def __grid__(self):
        """Wrapper for _permute_arrays."""
        axes = (ax.mid_points for ax in self.ref.values())
        self.grid = _permute_arrays(axes)
        self.size  = self.grid.size        # Update total size of grid.
        self.shape = self.grid.size        # Update shape of grid.  
            #self.x.mid_points, 
            #self.y.mid_points, 
            #self.z.mid_points))

    # def __index__(self, cloud):
    #     """Returns index of cell that contains input, if any, else None."""
    #     ix = np.where(np.logical_and(*[
    #         cloud[ax] for ax in ["x", "y", "z"]
    #         #self.min_bounds.__le__(float(value)), # Value less than x.
    #         #self.max_bounds.__gt__(float(value))  # Value greater than x.
    #     ]))[0]
    #     ix = None if len(ix) is 0 else ix[0]
    #     return(ix)