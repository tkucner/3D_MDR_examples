import numpy as np
arr = np.array([[0, 8, 0], [7, 0, 0], [-5, 0, 1]])

print ( arr)

out_tpl = np.array(np.nonzero(arr)).T
print(out_tpl)

for inds in out_tpl[:]:
    print(tuple(inds),arr[tuple(inds)])

