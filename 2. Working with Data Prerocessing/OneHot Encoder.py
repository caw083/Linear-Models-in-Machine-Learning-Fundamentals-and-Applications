import numpy as np

def onehot_encoding(X: np.ndarray) -> np.ndarray:
    # Get sorted unique values
    unique_values = np.sort(np.unique(X))
    
    # Map each value to its index in the sorted list
    value_to_index = {val: idx for idx, val in enumerate(unique_values)}
    
    # Create an empty matrix of shape (len(X), number of unique values)
    onehot = np.zeros((len(X), len(unique_values)), dtype=int)
    
    # Fill in the one-hot matrix
    for i, val in enumerate(X):
        onehot[i, value_to_index[val]] = 1
    
    return onehot