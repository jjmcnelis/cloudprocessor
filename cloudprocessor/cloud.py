import dask.dataframe as dd
import numpy as np

def _read_dask_df(file: str, options: dict={"sep": " ", "names" :None}):
    """Parse XYZ cloud to dask data frame."""
    try:
        return dd.read_csv(file, **options)
    except Exception as e:
        print("Error reading input cloud: %s" % file); raise(e)


def _merge_dask_df(df_to_merge, merge_to_df=None):
    """Merge (by appending) df_to_merge into (existing) merge_to_df."""  
    if type(df_to_merge) is list:  # If first arg is a list, concatenate.
        df_to_merge = dd.concat(df_to_merge)
    
    if merge_to_df is None: # If merge_to_df is None, return.
        return df_to_merge
    else:
        # Attempt to merge df_to_merge into merge_to_df. 
        try:                   
            df = dd.concat([merge_to_df, df_to_merge], axis=0)
            print("Successfully merged cloud.")

        # If failure, return existing df (merge_to_df).
        except Exception as e:                      
            print("Error merging cloud."); print(e)
            df = merge_to_df
        
        # Finally, if no exceptions, return merged df.
        finally:               
            return df    


def _compute_dask_df_bnds(merged):
    xbnds = merged.x.min().compute(), merged.x.max().compute()
    ybnds = merged.y.min().compute(), merged.y.max().compute()
    zbnds = merged.z.min().compute(), merged.z.max().compute()
    return(xbnds, ybnds, zbnds)    

    
class Cloud:
    """ """   
    
    ### Initialize Cloud attributes.
    clouds = {}
    merged = None
    
    ### Defaults: 3D scale and transformation matrix. 
    scale =  [1.0, 1.0, 1.0]        # Cloud scale       (x=1, y=1, z=1).
    trans =  [0.0, 0.0, 0.0]        # Cloud translation (None).
    rotat = [[1.0, 0.0, 0.0],       # Cloud rotation    (None).
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0]]
    
    ### Class instantiation. 

    def __init__(self, files: list=[], merge: bool=False):
        """Takes as input a list of paths to point clouds."""
        for f in files:             # Iterate over input point cloud files.
            merge = True if (len(files) <= 1) else merge
            self.__add__(f, merge)  # Add cloud to class.
    
    ### Class methods: point clouds. 
            
    def __add__(self, file: str, merge: bool=False):
        self.clouds[file] = _read_dask_df(file)
        # ADD LOGIC TO TRANSFORM IF MATRIX ISNT DEFAULT
        if merge:
            self.merged = _merge_dask_df(self.clouds[file], self.merged)
            self.__bounds__()

    def __merge__(self):
        self.merged = _merge_dask_df(list(self.clouds.values()), None)
        self.__bounds__()

    def __bounds__(self):
        xbnds, ybnds, zbnds  = _compute_dask_df_bnds(self.merged)
        self.xmin, self.xmax = xbnds
        self.ymin, self.ymax = ybnds
        self.zmin, self.zmax = zbnds

    def Index(self, xax=None, yax=None, zax=None):
        """Get per-axis arrays of cells containing each point in cloud."""
        self.merged["xi"] = self.merged.x.apply(xax.__ix__)
        self.merged["yi"] = self.merged.y.apply(yax.__ix__)
        self.merged["zi"] = self.merged.z.apply(zax.__ix__)
        self.merged = self.merged.compute()

        # Create and return decorated function to index cloud.
        def indexer(xi, yi, zi):
            return(self.merged.loc[ 
                (self.merged.xi == xi) & 
                (self.merged.yi == yi) &
                (self.merged.zi == zi) ])
        
        return(indexer)


    ### Class methods: transformation. 
    
    def __axis__(self, axis: str):
        """Returns the index of the axis name."""
        return {"x": 0, "y": 1, "z": 2}[axis]  # Return the axis number.                           

    def __scale__(self, axis: str, value: float):
        """Scale point cloud along input axis."""
        axix = self.__axis__(axis)            # Get the axis number
        self.scale[axix] = value               # Replace scale matrix value.
        print("...")                           # Translate cloud.       
        
    def __translate__(self, axis: str, value: float):
        """Positive or negative shift (translation) along input axis."""
        axix = self.__axis__(axis)            # Get the axis number
        self.trans[axix] = value               # Replace translate matrix val.
        print("...")                           # Translate cloud.
        
    def __rotate__(self, axis: str, matrix: list):
        """Rotate point cloud along input axis."""        
        axix = self.__axis__(axis)            # Get the axis number.
        self.rotat[axix] = matrix              # Replace rotation matrix row.
        print("...")                           # Rotate cloud.    

    def __matrix__(self, axis=None):
        """Returns transformation array for an axis or whole matrix."""    
        if axis is None:                       # If no axis given,
            return self.rotat + [self.trans]   # Merge and return matrix.
        else:                                  # Else if axis given,
            axix   = self.__axis__(axis)      # Get the axis number.
            rotat = self.rotat[axix]           # Get the rotation matrix.
            return rotat + [self.trans[axix]]  # Append the translation value.

