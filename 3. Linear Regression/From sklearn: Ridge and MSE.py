import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

def evaluation(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, fit_intercept=True, alpha=1.0) -> float:
    """
    Implements a Linear regression with L2 regularization (Ridge Regression)
    and evaluates its performance using the MSE metric.

    Args:
        X_train (np.ndarray): Features of the training dataset.
        y_train (np.ndarray): Target variable of the training dataset.
        X_test (np.ndarray): Features of the test dataset.
        y_test (np.ndarray): Target variable of the test dataset.
        fit_intercept (bool, optional): Whether to calculate the intercept. Defaults to True.
        alpha (float, optional): The regularization coefficient. Defaults to 1.0.

    Returns:
        float: The MSE metric value on the test dataset.
    """
    # Initialize the Ridge model with the given parameters
    model = Ridge(alpha=alpha, fit_intercept=fit_intercept)

    # Train the model on the training data
    model.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = model.predict(X_test)

    # Calculate the Mean Squared Error (MSE)
    mse = mean_squared_error(y_test, y_pred)

    return mse