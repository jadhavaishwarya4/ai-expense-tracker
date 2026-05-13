import numpy as np

from sklearn.linear_model import LinearRegression


def predict_expenses(data):

    x = np.array(
        range(len(data))
    ).reshape(-1, 1)

    y = np.array(data)

    model = LinearRegression()

    model.fit(x, y)

    next_month = np.array([[len(data)]])

    prediction = model.predict(next_month)

    return round(prediction[0], 2)