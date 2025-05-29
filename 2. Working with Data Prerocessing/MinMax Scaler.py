import numpy as np

def minmax_scale(X: np.ndarray) -> np.ndarray:
    # Convert input to float for division
    X = X.astype(float)
    
    # Calculate min and max for each column
    min_vals = X.min(axis=0)
    max_vals = X.max(axis=0)
    
    # Calculate range
    range_vals = max_vals - min_vals
    
    # Avoid division by zero by setting range to 1 where min == max
    # and set result to 0 in those columns
    scaled = np.where(range_vals != 0, (X - min_vals) / range_vals, 0)
    
    return scaled
