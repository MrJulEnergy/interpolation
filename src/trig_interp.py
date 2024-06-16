import numpy as np

def trigonometric_interpolation(points: np.array) -> np.array:
    n: int = points.shape[1] - 1
    print(n)
    d: int = points.shape[0]  # dimension
    t_i = np.array([2 * np.pi / (n + 1) * i for i in range(0, n + 2)])
    t = np.linspace(0, 2 * np.pi, 100+10*n)

    if n % 2 == 0:  # falls n gerade
        m = int(n / 2)
        theta = 0
    else:  # falls n ungerade
        m = int((n - 1) / 2)
        theta = 1

    fs = np.ndarray(shape=(d, len(t)))

    for dim in range(d):
        z = points[dim, :]
        a = np.array(
            [
                2 / (n + 1) * np.sum([z[j] * np.cos(j * t_i[k]) for j in range(n + 1)])
                for k in range(m + 2)
            ]
        )
        b = np.array(
            [
                2 / (n + 1) * np.sum([z[j] * np.sin(j * t_i[k]) for j in range(n + 1)])
                for k in range(1, m + 1)
            ]
        )

        f1 = a[0] / 2
        f2 = np.sum(
            [a[k] * np.cos(k * t) + b[k - 1] * np.sin(k * t) for k in range(1, m + 1)],
            axis=0,
        )
        f3 = theta / 2 * a[m+1] * np.cos((m + 1) * t)
        f = f1 + f2 + f3
        fs[dim, :] = f

    return fs