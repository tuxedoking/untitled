import numpy as np
a = np.arange(10, 22).reshape(3, 4)
print(a)
array = np.array([[1, 2, 3, 4, 5], [2, 3, 4, 5, 7]], dtype='uint8')
print(type(array))
print(array.dtype)
print(array.flags)
print(array.itemsize)
print(a)
print(np.sum(a))
print(np.nan)

