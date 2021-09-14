import numpy as np


def convolute(image, kernel):
    if not (isinstance(image, np.ndarray) and isinstance(kernel, np.ndarray)):
        return None
    if kernel.shape[0] > image.shape[0] or kernel.shape[1] > image.shape[1]:
        return None

    new_image = np.zeros((image.shape[0] - kernel.shape[0] + 1, image.shape[1] - kernel.shape[1] + 1), dtype=int)

    for y in range(new_image.shape[1]):
        for x in range(new_image.shape[0]):
            pixel = 0
            for i in range(kernel.shape[0]):
                for j in range(kernel.shape[1]):
                    pixel += kernel[i][j]*image[y + i][x + j]
            new_image[y][x] = pixel

    return new_image # (new_image/kernel.sum())*np.amax(image)
