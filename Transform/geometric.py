from math import cos, inf, sin
from .interpolation import interpolation
import numpy as np


class Geometric:
    minimum = [inf, inf]
    maximum = [-inf, -inf]
    size = [0, 0]
    o = [0, 0]
    cosine = 0
    sine = 0

    def __init__(self):
        pass

    def setDimensions(self, theta, current_size=None, new_size=None, o=None):

        self.cosine = cos(theta)
        self.sine = sin(theta)

        if current_size is not None:

            corners = [[0, 0], [0, current_size[1]], [current_size[0], current_size[1]], [current_size[0], 0]]

            for corner in corners:
                self.rotatePt(corner)
                self.minimum[0] = min(self.minimum[0], corner[0])
                self.minimum[1] = min(self.minimum[1], corner[1])
                self.maximum[0] = max(self.maximum[0], corner[0])
                self.maximum[1] = max(self.maximum[1], corner[1])

            self.size = [self.maximum[0] - self.minimum[0] + 1, self.maximum[1] - self.minimum[1] + 1]
            self.o = [-self.minimum[0], -self.minimum[1]]
        else:
            self.size[0] = int(new_size[0])
            self.size[1] = int(new_size[1])
            self.o[0] = int(o[0])
            self.o[1] = int(o[1])

    def rotatePt(self, pt, inverse=False):
        if inverse:
            new_x = int(pt[0] * self.cosine + pt[1] * self.sine)
            new_y = int(-pt[0] * self.sine + pt[1] * self.cosine)
        else:
            new_x = int(pt[0] * self.cosine - pt[1] * self.sine)
            new_y = int(pt[0] * self.sine + pt[1] * self.cosine)

        pt[0] = new_x
        pt[1] = new_y

    def respectToO(self, pt, inverse=False):
        if inverse:
            pt[0] -= self.o[0]
            pt[1] -= self.o[1]
        else:
            pt[0] += self.o[0]
            pt[1] += self.o[1]

    def forward_rotate(self, image, theta):
        self.setDimensions(theta, [len(image), len(image[0])])

        rotated_image = np.zeros((self.size[0], self.size[1], 3), np.uint8)

        for r in range(len(image)):
            for c in range(len(image[r])):
                prime = [r, c]
                self.rotatePt(prime)
                self.respectToO(prime)
                rotated_image[prime[0], prime[1]] = image[r, c]

        return rotated_image

    def reverse_rotation(self, rotated_image, theta, origin, original_shape):
        self.setDimensions(theta, new_size=original_shape, o=origin)

        original_image = np.zeros((self.size[0], self.size[1], 3), np.uint8)

        for r in range(len(rotated_image)):
            for c in range(len(rotated_image[r])):
                prime = [r, c]
                self.respectToO(prime, True)
                self.rotatePt(prime, True)

                if 0 <= prime[0] < original_shape[0] and 0 <= prime[1] < original_shape[1]:
                    original_image[prime[0], prime[1]] = rotated_image[r, c]

        return original_image

    def rotate(self, image, theta, interpolation_type):
        self.setDimensions(theta, [len(image), len(image[0])])

        rotated_image = np.zeros((self.size[0], self.size[1], 3), np.uint8)

        for r in range(len(rotated_image)):
            for c in range(len(rotated_image[r])):
                prime = [r, c]
                self.respectToO(prime, True)
                self.rotatePt(prime, True)
                if interpolation_type == 'bilinear':
                    rotated_image[r, c] = interpolation.bilinear_interpolation(prime, image)
                else:
                    rotated_image[r, c] = interpolation.linear_interpolation(prime, image)

        return rotated_image
