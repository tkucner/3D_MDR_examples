import numpy as np


class NDSparseMatrix:
    def __init__(self):
        self.elements = {}

    def from_dense(self, matrix):
        inds = np.array(np.nonzero(matrix)).T
        for ind in inds:
            self.addValue(tuple(ind), matrix[tuple(ind)])

    def addValue(self, tuple, value):
        self.elements[tuple] = value

    def readValue(self, tuple):
        try:
            value = self.elements[tuple]
        except KeyError:
            # could also be 0.0 if using floats...
            value = 0
        return value
