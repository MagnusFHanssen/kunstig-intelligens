# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:31:11 2020

@author: Bernt
"""

import numpy as np
import matplotlib.pyplot as plt


class Perceptron:
    def __init__(self, learning_rate=0.1):
        self.weights = np.zeros((3,))
        self.learning_rate = learning_rate
        self.training_error_history = []
        self.test_error_history = []

    def train(self, x_set, y_set):
        # shuffle data for each epoch
        train_data = np.hstack((x_set, y_set.reshape((len(y_set), -1))))
        np.random.shuffle(train_data)
        x_set, y_set = train_data[:, 0:2], train_data[:, 2]

        for x, y in zip(x_set, y_set):
            pred = self.predict(x)
            self.weights -= self.learning_rate * \
                            (pred - y) * \
                            np.array([x[0], x[1], 1.0])

        error_train2 = 0
        for x, y in zip(x_set, y_set):
            pred = self.predict(x)
            error_train2 += (pred - y) ** 2

        self.training_error_history.append(error_train2 / len(x_train))

        print('Updated weights: {}, Training MSE: {}'
              .format(self.weights,
                      self.training_error_history[-1]))

    def predict(self, x):
        return 1 if np.dot(x, self.weights[0:2]) + self.weights[2] >= 1 else 0

    def evaluate(self, x_set, y_set):
        test_error2 = 0

        for i in range(len(x_set)):
            test_error2 += (self.predict(x_set[i]) - y_set[i]) ** 2
        self.test_error_history.append(test_error2 / len(x_set))

        print('Testing MSE: {}'.format(self.test_error_history[-1]))

    def plot_error_histories(self):
        plt.plot(self.training_error_history, label='Training MSE')
        plt.plot(self.test_error_history, label='Test MSE')
        plt.legend()
        plt.xlabel('Training cycle')
        plt.grid(True)
        plt.show()


if __name__ == '__main__':
    # x train data
    x_train = np.array([[-10, 5],
                        [-10, 18],
                        [-9, 20],
                        [-5, 5],
                        [-3, 0],
                        [2, -3],
                        [5, -7],
                        [5, -8],

                        [5, -6],
                        [5, 0],
                        [4, 0],
                        [1, 0],
                        [1, 1],
                        [-2, 5],
                        [-3, 11],


                        ])

    # y train data
    y_train = np.array([1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0])

    # x test data
    x_test = np.array([[2.2, 3.2],
                       [8.2, 8.1],
                       [7.1, 8.7],
                       [6.2, 7.3],
                       ])

    # y test data
    y_test = np.array([1, 0, 0, 0])

    p = Perceptron(learning_rate=0.001)

    epochs = 250
    for e in range(epochs):
        p.train(x_train, y_train)
        p.evaluate(x_test, y_test)

    p.plot_error_histories()

    # plot data and separating line
    w1, w2, b = p.weights
    class1 = np.vstack((x_train[:8, :], x_test[:8, :]))
    class2 = np.vstack((x_train[8:, :], x_test[8:, :]))

    plt.scatter(class1[:, 0], class1[:, 1], c='red', label='Label 1')
    plt.scatter(class2[:, 0], class2[:, 1], c='blue', label='Label 2')

    x = np.linspace(0, 7, 100)
    y = (1 - b) / w2 - w1 * x / w2
    print('weights ', w2, w1)
    plt.grid(True)
    plt.legend()
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.plot(x, y, color='black')

    plt.show()