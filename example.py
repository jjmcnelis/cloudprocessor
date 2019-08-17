#!/usr/bin/bash
import cloudprocessor as cp

if __name__ == "__main__":

    # Read an input xyz space-delimited point cloud to Cloud object.
    myCloud = cp.Cloud(["tests/tls1.xyz"])

    # Add a second cloud. This will not merge it with base cloud.
    myCloud.__add__("tests/tls2.xyz")

    # Merge the two.
    myCloud.__merge__() 

    print(myCloud.merged)