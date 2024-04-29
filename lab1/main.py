import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
import math
from utils import *

def interactive_dois_dois():
    N = int(input("Enter N: "))
    lam = int(input("Enter lambda: "))
    return dois_dois(N, lam)

def dois_dois(N=120, lam=3):
    # Step 1: Generate sequence of events
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
    N = 5000
    KIND_OF_N = 5000
    lambdas = [3, 7, 13, 15]
    N_temp = N*len(lambdas)
    N_arr = [int(N_temp*lam//sum(lambdas)) for lam in lambdas]

    events = [[], []]
    events_theoretical = []

    for idx in range(len(lambdas)):
        tmp = generate_events(N_arr[idx], lambdas[idx])
        events[0].extend(tmp[0])
        events[1].extend(tmp[1])

    hist = events_to_poisson(events)

    unique_x = [x for x in hist.keys()]
    unique_x.sort()

    y = [0 for _ in unique_x]
    y_sum = poisson.pmf(unique_x, mu=sum(lambdas))
    plt.plot(unique_x, y_sum, 'r--')

    for lam in lambdas:
        new_y = poisson.pmf(unique_x, mu=lam)
        y = [y[i] + new_y[i] for i in range(len(y))]
    y = [y[i]/len(lambdas) for i in range(len(y))]

    # Experimental data
    counts = sum(hist.values())
    y = [hist[x]/counts for x in unique_x]
    plt.bar(unique_x, y, width=1, align='center')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    # interactive_dois_dois()
    # dois_dois(N=20000, lam=30)
    dois_tres()
