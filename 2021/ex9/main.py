import numpy as np
from convolution import convolute

kernel = np.array([[1, 0, 2],
                   [2, 1, 0],
                   [0, 2, 1]])


image = np.array([[0, 2, 3, 3, 4, 0],
                  [0, 0, 1, 1, 0, 0],
                  [0, 1, 4, 1, 0, 0],
                  [0, 0, 2, 3, 0, 0],
                  [0, 0, 1, 3, 0, 0],
                  [0, 0, 1, 1, 0, 0]])

new_image = convolute(image, kernel)

print(np.round(new_image))

