import numpy as np


def _get_permuted_arrays(arrays):
    """Generate an array of voxel centroids from three dimensional arrays."""  
    arrays = [np.asarray(x) for x in arrays]  # Ensure all inputs are arrays.
    shape  = (len(x) for x in arrays)         # Get shape of each as a tuple.    
    ndims  = np.indices(shape)                # Get shape as array.
    index  = ndims.reshape(len(arrays), -1).T # Transpose.
    
    # Create empty 3d array, add axis positions, return.
    voxels = np.empty_like(index, dtype=arrays[0].dtype)
    for n, arr in enumerate(arrays):
        voxels[:, n] = arrays[n][index[:, n]]    
    return(voxels)


class Grid:
    """Initializes a grid for two or more axes."""
    
    def __init__(self, x=None, y=None, z=None):
        self.x, self.y, self.z = x, y, z     # Initialize input axes.
        self.__grid__()                      # Permute axes arrays.           

    def __grid__(self):
        """Wrapper for _get_permuted_arrays."""
        self.grid = _get_permuted_arrays((
            self.x.mid_points, 
            self.y.mid_points, 
            self.z.mid_points))
        
    def __add__(self, axis):
        """Add new Axis instance to grid."""
        setattr(self, axis.name, axis)