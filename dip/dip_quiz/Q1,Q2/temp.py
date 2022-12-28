import numpy as np

x = np.random.random_integers(0,5,(20,8))
print(x)
print()
print(np.median(x[0:3,0:3]))