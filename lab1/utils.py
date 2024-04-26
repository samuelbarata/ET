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
    print(events)
    return events, events_cumulative

def events_to_poisson(events):
    current_time = 0
    poisson_counts = []
    for i in events:
        current_time += i
        poisson_counts.append(math.floor(current_time))

    return poisson_counts

# def events_to_poisson(events, interval=1):
#     counts = np.zeros(len(interval)-1)
#     for event in events:
#         for i in range(len(interval)-1):
#             if interval[i] <= event < interval[i+1]:
#                 counts[i] += 1
#                 break
#     return counts


def histogram(data):
    histogram = {}
    for value in data:
        histogram[value] = histogram.get(value, 0) + 1
    return histogram
