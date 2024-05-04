import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
import math
from utils import *

def interactive_dois_dois():
    N = int(input("Enter N: "))
    lam = float(input("Enter lambda: "))
    return dois_dois(N, lam)

def dois_dois(N=120, lam=3):
    # Step 1: Generate sequence of events
    hist = events_to_poisson(generate_events(N, lam))

    # Calculate corresponding y values
    unique_x = [x for x in hist.keys()]
    unique_x.sort()

    y = [0 for _ in unique_x]
    y_sum = poisson.pmf(unique_x, mu=lam)
    theo = plt.plot(unique_x, y_sum, 'r--', label='Theoretical')

    # y = poisson.pmf(unique_x, mu=lam)
    # plt.stem(unique_x, y, 'r--', label='Theoretical')

    # Experimental data
    counts = sum(hist.values())
    y = [hist[x]/counts for x in unique_x]
    exp = plt.bar(unique_x, y, width=1, align='center', label='Experimental')
    plt.legend(handles=[theo[0], exp])
    plt.xlabel('Number of events')
    plt.ylabel('Frequency')
    plt.title(f'{N} events with rate {lam}')
    plt.grid(True)
    plt.show()

def dois_tres(N=5000, lambdas=[3, 7, 13, 15]):
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
    theo = plt.plot(unique_x, y_sum, 'r--', label='Theoretical')

    for lam in lambdas:
        new_y = poisson.pmf(unique_x, mu=lam)
        y = [y[i] + new_y[i] for i in range(len(y))]
    y = [y[i]/len(lambdas) for i in range(len(y))]

    # Experimental data
    counts = sum(hist.values())
    y = [hist[x]/counts for x in unique_x]
    exp = plt.bar(unique_x, y, width=1, align='center', label='Experimental')
    plt.xlabel('Number of events')
    plt.ylabel('Frequency')
    plt.title(f'Total of {N} events with rates {lambdas}')
    plt.legend(handles=[theo[0], exp])
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    #interactive_dois_dois()
    report = ((10,1), (1000, 1), (10000, 1), (50000, 1),
    (10,5), (1000, 5), (10000, 5), (50000, 5),
    (10,20), (1000, 20), (10000, 20), (50000, 20))
    for N, lam in report:
        dois_dois(N, lam)

    for N in [100, 5000, 50000, 500000]:
        dois_tres(N=N)
