import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
import math
from utils import *

def dois_dois():
    # Step 1: Generate sequence of events
    N = 120
    lam = 3
    events = generate_poisson(N, lam)
    # TODO: I tried, but cant get this to work; but we do need to generate evens using the exponential thingy... [I think]
    # events = events_to_poisson(generate_events(N, lam)[0])

    hist = histogram(events)

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

    hist = histogram(events)
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
    dois_dois()
    # dois_tres()
