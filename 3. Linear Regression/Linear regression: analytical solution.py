import numpy as np

def analytical_solution(X: np.ndarray, y: np.ndarray, fit_intercept: bool = True) -> np.ndarray:

    if fit_intercept:
        # Add a column of ones to X for the intercept term.
        # This allows us to calculate the intercept as part of the weight vector.
        X = np.hstack((np.ones((X.shape[0], 1)), X))
  
    # Calculate the weights using the formula: w = (X^T * X)^-1 * X^T * y.
    weights =  np.linalg.inv(X.T @ X) @ X.T @ y

    return weights