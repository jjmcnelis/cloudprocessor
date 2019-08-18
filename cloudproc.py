import dask.dataframe as dd
import dask.array as da
import numpy as np
import sys


def _safe_arange(start, stop, step):
    return step * np.arange(start / step, stop / step)


def _get_axis_mids(res: float, min: float, max: float):
    """Get centers of cells on an input axis defined by its min, max, res.
    
    This necessarily convoluted routine ensures that all discrete points in a 
    point cloud will all fall inside the returned axis (cell centers) with
    the specified resolution.
    
    :param min: The minimum of all point positions along this axis.
    :type min: float.
    :param max: The maximum of all point positions along this axis.
    :type max: float.
    :param res: The resolution of the desired axis (centers) array.
    :type res: float.
    :returns:  numpy.array.
    
    """
    midpoint       = (max + min)*0.5
    sequence_left  = _safe_arange(midpoint - res, min - res, -res)
    sequence_right = _safe_arange(midpoint, max + res, res)
    midpoints      = np.concatenate([np.sort(sequence_left), sequence_right])
    return midpoints


class Axis:
    """The arrays and attributes that fully describe a cartesian axis.
    
    .. note::
        All attributes WITHOUT underscores describe axis properties.
        All attributes WITH underscores describe cell properties.    
    
    """
    
    def __init__(self, name: str, res: float, min: float, max: float):
        """Initializes an `Axis` class object.
        
        :param name: The name of this axis. Best to use one of [x, y, z].
        :type name: str.       
        :param min: The minimum of all point positions along this axis.
        :type min: float.
        :param max: The maximum of all point positions along this axis.
        :type max: float.
        :param res: The resolution of the desired axis (centers) array.
        :type res: float.

        """
        # Axis properties.
        self.name = name
        self.min  = float(min)
        self.max  = float(max)
        self.res  = float(res)

        # Cell properties (positions on the axis).
        self.mid_points = _get_axis_mids(self.res, self.min, self.max)
        self.min_bounds = self.mid_points - self.res*0.5
        self.max_bounds = self.mid_points + self.res*0.5        
        
        # More axis properties.
        self.mid  = (self.min + self.max)*0.5
        self.size = self.mid_points.size

    def __shift__(self, shift: float):
        """Shift the axis by the input float (positive or negative)."""
        self.midpoint   = self.midpoint + float(shift)
        self.mid_points = self.mid_points + float(shift)
        self.min_bounds = self.min_bounds + float(shift)
        self.max_bounds = self.max_bounds + float(shift)
    
    def __on__(self, value: float):
        """Tests if input value exists on the axis (within min, max)."""
        return((self.min < value) & (value < self.max))
    
    def __ix__(self, value: float):
        """Returns index of cell that contains input, if any, else None."""
        ix = np.where(np.logical_and(
            self.min_bounds.__le__(float(value)),     # Value less than x.
            self.max_bounds.__gt__(float(value))))[0] # Value greater than x.
        ix = None if len(ix) is 0 else ix[0]
        return(ix)


def _read_xyz(file: str, options: dict={"sep": " ", "names" :None}):
    """Parse XYZ cloud to dask data frame."""
    try:
        return dd.read_csv(file, **options)
    except Exception as e:
        print("Error reading input cloud: %s" % file); raise(e)

def _merge_xyz(xyz_data_frames: list):
    """Try to merge xyz data frames."""  
    try: 
        df = dd.concat(xyz_data_frames, axis=0)
        return df
    except Exception as e:
        raise(e)

def _range_xyz(cloud):
    """Get min and max of each cloud axis."""
    xbnds = cloud.x.min().compute(), cloud.x.max().compute()
    ybnds = cloud.y.min().compute(), cloud.y.max().compute()
    zbnds = cloud.z.min().compute(), cloud.z.max().compute()
    return(xbnds, ybnds, zbnds)    

def _permute_xyz(arrays):
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


class Cloud:
    """A basic point cloud class."""
    
    #Default 4x4 transformation matrix (no rotation or translation):    
    rotat = [[1.0, 0.0, 0.0], # <- Cloud rotation for axes: x,
             [0.0, 1.0, 0.0], # <-                          y,
             [0.0, 0.0, 1.0]] # <-                          z
    trans =  [0.0, 0.0, 0.0]  # <- Cloud translation x, y, z; (Also none).
    
    # Cloud scale (scale to integers for big clouds).
    scale =  [1.0, 1.0, 1.0]  # <- Cloud scale (x=1, y=1, z=1).

    def __init__(self, file: str=None):
        self.data = _read_xyz(file)            # Get dask data frame.
        self.bnds = _range_xyz(self.data)      # Get range of each axis.

    def __axis__(self, axis: str):
        """Returns the index of the axis name."""
        return {"x": 0, "y": 1, "z": 2}[axis]  # Return the axis number.                           

    def __scale__(self, axis: str, value: float):
        """Scale point cloud along input axis."""
        axix = self.__axis__(axis)             # Get the axis number
        self.scale[axix] = value               # Replace scale matrix value.
        print("...")                           # Translate cloud.       
        
    def __translate__(self, axis: str, value: float):
        """Positive or negative shift (translation) along input axis."""
        axix = self.__axis__(axis)             # Get the axis number
        self.trans[axix] = value               # Replace translate matrix val.
        print("...")                           # Translate cloud.
        
    def __rotate__(self, axis: str, matrix: list):
        """Rotate point cloud along input axis."""        
        axix = self.__axis__(axis)             # Get the axis number.
        self.rotat[axix] = matrix              # Replace rotation matrix row.
        print("...")                           # Rotate cloud.    

    def __matrix__(self, axis=None):
        """Returns transformation array for an axis or whole matrix."""    
        if axis is None:                       # If no axis given,
            return self.rotat + [self.trans]   # Merge and return matrix.
        else:                                  # Else if axis given,
            axix   = self.__axis__(axis)       # Get the axis number.
            rotat = self.rotat[axix]           # Get the rotation matrix.
            return rotat + [self.trans[axix]]  # Append the translation value.


class Dataset:
    """ """

    # Instances of class Cloud + merged clouds' index:
    clouds = {}
    index  = None
    
    # Instances of class Axis (apply to all clouds together).
    x = None                             # Merged x axis,
    y = None                             # ... y axis, and
    z = None                             # ... z axis.
    xax, yax, zax = None, None, None     # Axis objects for each.
    
    def __init__(self, files: list=None):
        """Takes list of paths to clouds, reads, makes a 'virtual' merge."""
        if files is not None:            # If files given,
            for f in files:              # iterate over them, 
                self.__add__(f, False)   # add cloud as attribute.
        self.__update__()                # Update bounds and Axis attributes.

    def __merge__(self):
        return(_merge_xyz(list(self.clouds.values())))

    def __add__(self, file: str, update: bool=True):
        self.clouds[len(self.clouds.keys())] = Cloud(file)
        if update: 
            self.__update__()

    def __update__(self):
        merge = self.__merge__()         # Merge the clouds.
        bnds = _range_xyz( merge.data )  # Get the limits of each axis: x y z.
        self.bnds = dict(x=bnds[0], y=bnds[1], z=bnds[2])

    def __fit__(self, axes: dict):       #  !!!
        """!!! WRITE A WRAPPER !!! Takes dict( x=res, y=res, z=res )."""
        merge = self.__merge__()         # Merge the clouds.
        for ax, res in axes.items():     # Interate over input axes dict.
            amin, amax = self.bnds[ax]   # Get min and max of cloud for axis.
            setattr(self, ax, merge.data[ax])                 # Set array.
            setattr(self, ax+"ax", Axis(ax, res, amin, amax)) # Set instance.
    
    def __ix__(self):
        """Index cloud according to xax, yax, zax."""
        self.xix = self.x.apply(self.xax.__ix__)
        self.yix = self.y.apply(self.yax.__ix__)
        self.zix = self.z.apply(self.zax.__ix__)

    def __sel__(self, xyz):
        """Select points from the cloud according to input x, y, z index."""
        six = ((self.xix==xyz[0]) & (self.yix==xyz[1]) & (self.zix==xyz[2]))
        return(self.x[six], self.y[six], self.z[six])

    def __stat__(self, stat="mean"):
        """!!! WRITE A WRAPPER !!! """
        xixunq = np.sort(self.xix.unique())
        yixunq = np.sort(self.yix.unique())
        zixunq = np.sort(self.zix.unique())

        voxels = _permute_xyz((xixunq, yixunq, zixunq))
        x,y,z  = self.__sel__(voxels)
        return(np.nanmean(x), np.nanmean(y), np.nanmean(z))


if __name__ == "__main__":
    
    print(sys.argv)
    XYZ = "tests/tls1.xyz"
    DS = Dataset([XYZ])
    DS.__fit__({"x": 1, "y": 1, "z": 1})
    DS.__ix__()
    DS.__stat__()






#def Index(self, xax=None, yax=None, zax=None):
    #    """Get per-axis arrays of cells containing each point in cloud."""
        #self.merged["xi"] = self.merged.x.apply(xax.__ix__)
        #self.merged["yi"] = self.merged.y.apply(yax.__ix__)
        #self.merged["zi"] = self.merged.z.apply(zax.__ix__)
        #self.merged = self.merged.compute()

        # Create and return decorated function to index cloud.
        #def indexer(xi, yi, zi):
        #    return(self.merged.loc[ 
        #        (self.merged.xi == xi) & 
        #        (self.merged.yi == yi) &
        #        (self.merged.zi == zi) ])
        
        #return(indexer)

