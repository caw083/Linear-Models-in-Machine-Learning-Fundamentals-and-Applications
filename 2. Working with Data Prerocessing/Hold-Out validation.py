import numpy as np

def train_test_split(X: np.ndarray, y: np.ndarray, test_size=0.33):
    # Set random seed for reproducibility
    np.random.seed(1234)
    
    # Total number of samples
    n_samples = X.shape[0]
    
    # Calculate number of test samples
    n_test = round(test_size * n_samples)
    
    # Generate shuffled indices
    indices = np.arange(n_samples)
    np.random.shuffle(indices)
    
    # Get test and train indices
    test_indices = indices[:n_test]
    train_indices = indices[n_test:]
    
    # Split the data
    X_test = X[test_indices]
    y_test = y[test_indices]
    X_train = X[train_indices]
    y_train = y[train_indices]
    
    return X_train, y_train, X_test, y_test
