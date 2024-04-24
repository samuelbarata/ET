import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
import math

def generate_poisson(N=120, lam=3):
    rng = np.random.default_rng()
    return rng.poisson(lam=lam, size=N)

def dumbest_histogram_in_existence(data):
    histogram = {}
    for value in data:
        if value in histogram:
            histogram[value] += 1
        else:
            histogram[value] = 1
    return histogram

def dois_dois():
    # Step 1: Generate sequence of events
    N = 1200
    lam = 30
    events = generate_poisson(N, lam)

    hist = dumbest_histogram_in_existence(events)

    # Calculate corresponding y values
    unique_x = [x for x in hist.keys()]
    unique_x.sort()

    y = N * poisson.pmf(unique_x, mu=lam)
    plt.stem(unique_x, y, 'r--', label='Theoretical')

    # Experimental data
    y = [hist[x] for x in unique_x]
    plt.bar(unique_x, y, width=1, align='center')
    plt.grid(True)
    plt.show()

def dois_tres():
    lambdas = [3, 7, 13, 15]
    N = 1200
    events = []
    events_theoretical = []

    for lam in lambdas:
        events.extend(generate_poisson(N, lam))

    hist = dumbest_histogram_in_existence(events)
    unique_x = [x for x in hist.keys()]
    unique_x.sort()

    y = [0 for _ in unique_x]
    for lam in lambdas:
        new_y = N * poisson.pmf(unique_x, mu=lam)
        y = [y[i] + new_y[i] for i in range(len(y))]

    plt.plot(unique_x, y, 'r--', label='Theoretical')

    # Experimental data
    y = [hist[x] for x in unique_x]
    plt.bar(unique_x, y, width=1, align='center')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    # dois_dois()
    dois_tres()
