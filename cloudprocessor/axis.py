import numpy as np

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
    
    
    def __index__(self, value: float):
        """Returns index of cell that contains input, if any, else None."""
        ix = np.where(np.logical_and(
            self.min_bounds.__le__(float(value)),     # Value less than x.
            self.max_bounds.__gt__(float(value))))[0] # Value greater than x.
        ix = None if len(ix) is 0 else ix[0]
        return(ix)
