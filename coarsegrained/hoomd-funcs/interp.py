import numpy as np

def linear_interp(arr, step=1):
    # Clean up input -- sort and ensure that the array is N x 2
    arr= sorted(arr, key=lambda a: a[0])
    arr = np.array(arr)
    assert len(arr.shape) == 2
    assert arr.shape[1]  == 2

    # Get the x values
    minx = arr[0, 0]
    maxx = arr[-1, 0]
    x = np.arange(minx, maxx, step)

    # Linearly interpolate
    y = np.interp(x, arr[:,0], arr[:,1])

    # Return as a tuple
    out = list(zip(x, y))
    out.append(tuple(arr[-1]))
    return out
