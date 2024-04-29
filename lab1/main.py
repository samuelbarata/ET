import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
import math
from utils import *

def dois_dois():
    # Step 1: Generate sequence of events
    N = 12000
    lam = 3

    hist = events_to_poisson(generate_events(N, lam))

    # Calculate corresponding y values
    unique_x = [x for x in hist.keys()]
    unique_x.sort()

    y = poisson.pmf(unique_x, mu=lam)
    plt.stem(unique_x, y, 'r--', label='Theoretical')

    # Experimental data
    counts = sum(hist.values())
    y = [hist[x]/counts for x in unique_x]
    plt.bar(unique_x, y, width=1, align='center')
    plt.grid(True)
    plt.show()

def dois_tres():
    lambdas = [3, 7, 13, 15]
    N = 12000
    events = []
    events_theoretical = []

    for lam in lambdas:
        tmp = generate_events(N, lam)
        if len(events) == 0:
            events.append([x for x in tmp[0]])
            events.append([x for x in tmp[1]])
        else:
            events[0].extend(tmp[0])
            events[1].extend(tmp[1])

    hist = events_to_poisson(events)
    unique_x = [x for x in hist.keys()]
    unique_x.sort()

    y = [0 for _ in unique_x]
    for lam in lambdas:
        new_y = poisson.pmf(unique_x, mu=lam)
        y = [y[i] + new_y[i] for i in range(len(y))]

    plt.plot(unique_x, y, 'r--', label='Theoretical')

    # Experimental data
    counts = sum(hist.values())
    y = [hist[x]/counts for x in unique_x]
    plt.bar(unique_x, y, width=1, align='center')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    # dois_dois()
    dois_tres()
