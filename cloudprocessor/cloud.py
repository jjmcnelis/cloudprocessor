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

    
class Cloud:
    """ """   
    
    ### Initialize empty cloud as a dask dataframe. 
    
    merged = None
    clouds = {}
    
    ### Defaults: 3D scale and transformation matrix. 
    
    scale =  [1.0, 1.0, 1.0]    # Cloud scale       (x=1, y=1, z=1).
    trans =  [0.0, 0.0, 0.0]    # Cloud translation (None).
    rotat = [[1.0, 0.0, 0.0],   # Cloud rotation    (None).
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0]]
    
    
    ### Class instantiation. 
    
    def __init__(self, 
                 files: list=[], 
                 merge: bool=False, 
                 transform: list=None):
        """Takes as input a list of paths to point clouds."""
        # ADD LOGIC TO -----------> # Update the transformation matrix.
        for f in files:             # Iterate over input point cloud files.
            merge = True if (len(files) <= 1) else merge
            self.__add__(f, merge)  # Add cloud to class.
    

    ### Class methods: point clouds. 
            
    def __add__(self, file: str, merge: bool=False):
        """Parse XYZ cloud, apply transform, and append to class cloud."""
        self.clouds[file] = _read_dask_df(file)
        if merge:
            self.merged = _merge_dask_df(self.clouds[file], self.merged)

    def __merge__(self):
        self.merged = _merge_dask_df(list(self.clouds.values()), None)

    def __compute__(self):
        self.merged = self.merged.compute()    # Compute dask queue.

    
    ### Class methods: transformation. 
    
    def __index__(self, axis: str):
        """Returns the index of the axis name."""
        return {"x": 0, "y": 1, "z": 2}[axis] # Return the axis number.                           

    def __scale__(self, axis: str, value: float):
        """Scale point cloud along input axis."""
        axix = self.__index__(axis)           # Get the axis number
        self.scale[axix] = value              # Replace scale matrix value.
        print("...")                          # Translate cloud.       
        
    def __translate__(self, axis: str, value: float):
        """Positive or negative shift (translation) along input axis."""
        axix = self.__index__(axis)           # Get the axis number
        self.trans[axix] = value              # Replace translate matrix val.
        print("...")                          # Translate cloud.
        
    def __rotate__(self, axis: str, matrix: list):
        """Rotate point cloud along input axis."""        
        axix = self.__index__(axis)           # Get the axis number.
        self.rotat[axix] = matrix             # Replace rotation matrix row.
        print("...")                          # Rotate cloud.    

    def __matrix__(self, axis=None):
        """Returns transformation array for an axis or whole matrix."""    
        if axis is None:                      # If no axis given,
            return self.rotat + [self.trans]  # Merge and return matrix.
        else:                                 # Else if axis given,
            axix   = self.__index__(axis)     # Get the axis number.
            rotat = self.rotat[axix]          # Get the rotation matrix.
            return rotat + [self.trans[axix]] # Append the translation value.