import numpy as np


class interpolation:

    @staticmethod
    def linear_interpolation(pt, original):
        if 0 <= pt[0] < len(original) and 0 <= pt[1] < len(original[0]):
            return original[pt[0], pt[1]]

        return np.zeros(3, np.uint8)

    @staticmethod
    def bilinear_interpolation(pt, original):
        closest = np.zeros(3, np.uint)

        closest += interpolation.linear_interpolation(pt, original)
        pt[0] += 1
        closest += interpolation.linear_interpolation(pt, original)
        pt[1] += 1
        closest += interpolation.linear_interpolation(pt, original)
        pt[0] -= 1
        closest += interpolation.linear_interpolation(pt, original)

        return closest / 4
