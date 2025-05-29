import numpy as np

def calculate_r2(y_true, y_pred):
    """
    Calculates the R^2 (coefficient of determination) metric.

    Args:
        y_true (list or np.array): True values of the target feature.
        y_pred (list or np.array): Predicted values of the target feature.

    Returns:
        float: The calculated R^2 value.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    y_true_mean = np.mean(y_true)

    # Sum of squared residuals
    ss_res = np.sum((y_true - y_pred)**2)

    # Total sum of squares
    ss_tot = np.sum((y_true - y_true_mean)**2)

    # Handle the case where ss_tot is zero to avoid division by zero.
    # This typically means all true values are the same.
    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0

    r2 = 1 - (ss_res / ss_tot)
    return r2

if __name__ == "__main__":
    # Read true values from the first input line
    y_true_input = list(map(float, input().split()))
    # Read predicted values from the second input line
    y_pred_input = list(map(float, input().split()))

    # Calculate R^2 value
    r2_value = calculate_r2(y_true_input, y_pred_input)

    # Print the result formatted to two decimal places
    print(f"R2: {r2_value:.2f}")