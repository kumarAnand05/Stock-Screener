from sklearn.linear_model import LinearRegression
import numpy as np

def linear_regression(data):
    """
    Perform linear regression on the given data.
    Returns:
        regression model obejct
    """
    model = LinearRegression()
    data = data.to_numpy()  # Convert DataFrame to NumPy array

    x = np.arange(len(data)).reshape(-1, 1)  # Independent variable (time index)
    y = data.reshape(-1, 1)  # Dependent variable (data values)

    model.fit(x, y)
    return model

def regression_slope(model):
    """
    Get the slope of the regression line from the model.
    Returns:
        slope value
    """
    return round(model.coef_[0][0],2)