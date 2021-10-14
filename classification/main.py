# Imports
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('data.csv')
x1 = data.iloc[:, 0]
x2 = data.iloc[:, 1]
plt.scatter(x1, x2)


m = 0
c = 0

L = 0.0001 # Learning rate
epochs = 10000

n = float(len(x1))

# Gradient descent:
for i in range(epochs):
    pred_x2 = m * x1 + c # Predicted value of x2 as function of x1
    D_m = (-2/n) * sum(x1 * (x2 - pred_x2))
    D_c = (-2/n) * sum(x2 - pred_x2)
    m -= L * D_m
    c -= L * D_c

trend_x1 = np.linspace(0, 17, 10)
trend_x2 = m * trend_x1 + c
plt.plot(trend_x1, trend_x2, linestyle=':', color='r')
plt.show()

print("x2 = %.3f * x1 + %.3f" % (m, c))

# This program was adapted from the code shown on the webpage
# "https://towardsdatascience.com/linear-regression-using-gradient-descent-97a6c8700931"
# by Adarsh Menon, Sep 16, 2018. Date of visit: May 10, 2021 
