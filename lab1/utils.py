import numpy as np
import math

def generate_poisson(N=120, lam=3):
    rng = np.random.default_rng()
    return rng.poisson(lam=lam, size=N)

def generate_events(N, lambda_param):
    events_cumulative = []
    current_time = 0
    rng = np.random.default_rng()
    events = rng.exponential(scale=1/lambda_param, size=N)
    for delta_t in events:
        current_time += delta_t
        events_cumulative.append(current_time)
    return events, events_cumulative

def events_to_poisson(events):
    poisson_counts = []
    for value in events[1]:
        poisson_counts.append(math.floor(value))

    # Count how many values are repeated x times
    #[0,0,3,3,4] -> {2:2, 1:1} the number of pairs is 2, the number of singles is one
    counts_but_for_real = {}
    unique = set(poisson_counts)
    for value in unique:
        cnt = poisson_counts.count(value)
        counts_but_for_real[cnt] = counts_but_for_real.get(cnt, 0) + 1

    return counts_but_for_real


def histogram(data):
    histogram = {}
    for value in data:
        histogram[value] = histogram.get(value, 0) + 1
    return histogram
