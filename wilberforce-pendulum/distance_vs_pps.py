import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

x = np.arange(40)  # Distance from 0 to 39
y = np.array([
    1.417972177, 1.549037325, 1.295869762, 1.053192361, 0.9112457912, 0.823756809, 0.80768469,
    0.8552784899, 0.8229111929, 0.84831, 0.8669751301, 0.8874255252, 0.8651788444, 0.873806,
    0.84, 0.8197072474, 0.8603587759, 0.8340202323, 0.8164213788, 0.8033755274, 0.7901761879,
    0.7257318952, 0.7299630086, 1.137273, 1.130163, 1.059863, 1.035333, 1.035912, 1.049125,
    0.952703, 0.879755, 0.851351, 0.8159, 0.761194, 0.75, 0.696429, 0.5, 0.454545, 0.342857,
    0.391304
])

# Step 1: Choose the degree of the polynomial
degree = 5 

# Step 2: Transform x into polynomial features
poly = PolynomialFeatures(degree)
x_poly = poly.fit_transform(x.reshape(-1, 1))

# Step 3: Fit the model
model = LinearRegression()
model.fit(x_poly, y)

# Step 4: Make predictions
y_pred = model.predict(x_poly)

coefficients = model.coef_
intercept = model.intercept_
print(f"Coefficients: {coefficients}")
print(f"Intercept: {intercept}")

mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Step 5: Plot the data and the polynomial fit
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color="blue", label="Data points")  # Original data
plt.plot(x, y_pred, color="red", label=f"Polynomial fit (degree {degree})")  # Polynomial fit
plt.xlabel("Distance")
plt.ylabel("PPS")
plt.title("Distance vs. PPS: Polynomial Regression")
plt.legend()
plt.grid(True)
plt.show()