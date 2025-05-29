import numpy as np
import math

def calculate_regression_metrics(true_values, predicted_values):
    """
    Calculates Mean Squared Error (MSE), Mean Absolute Error (MAE), and
    Root Mean Squared Error (RMSE) between true and predicted values.

    Args:
        true_values (list or np.array): The true values of the target feature.
        predicted_values (list or np.array): The predicted values of the target feature.

    Returns:
        tuple: A tuple containing MSE, MAE, and RMSE, rounded to two decimal places.
    """
    true_values = np.array(true_values)
    predicted_values = np.array(predicted_values)

    # Ensure the input arrays have the same length
    if len(true_values) != len(predicted_values):
        raise ValueError("True and predicted values must have the same number of elements.")

    n = len(true_values)

    # Calculate MSE
    mse = np.sum((true_values - predicted_values)**2) / n

    # Calculate MAE
    mae = np.sum(np.abs(true_values - predicted_values)) / n

    # Calculate RMSE
    rmse = math.sqrt(mse)

    return round(mse, 2), round(mae, 2), round(rmse, 2)

if __name__ == "__main__":
    true_str = input()
    predicted_str = input()

    true_values = [float(x) for x in true_str.split()]
    predicted_values = [float(x) for x in predicted_str.split()]

    mse, mae, rmse = calculate_regression_metrics(true_values, predicted_values)

    print(f"MSE: {mse:.2f}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")