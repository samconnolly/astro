import numpy as np

a = [4, 3, 5, 7, 6, 8]
indices = [0., 1., 4.]
b = np.take(a, indices)

print b
