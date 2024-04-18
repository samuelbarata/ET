import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson


def generate_poisson_events(N, lambd):
    events = np.zeros(N)
    events_time = np.zeros(N)
    current_time = 0
    for i in range(N):
        delta_t = np.random.exponential(1 / lambd)
        current_time += delta_t
        events[i] = delta_t
        events_time[i] = current_time
    return events, events_time

def generate_poisson_events(N, lambd):
    events = np.random.exponential(1 / lambd, N)
    return events, []

def calculate_histogram(data, num_bins):
    # Calculate histogram bins
    min_val = np.min(data)
    max_val = np.max(data)
    bin_edges = np.linspace(min_val, max_val, num_bins + 1)

    # Count occurrences in each bin manually
    bin_counts = np.zeros(num_bins)
    for d in data:
        for i in range(num_bins):
            if bin_edges[i] <= d < bin_edges[i+1]:
                bin_counts[i] += 1
                break

    return bin_edges, bin_counts

if __name__ == '__main__':
    # Parameters
    N = 12000  # Number of events
    lambd = 3  # Rate parameter

    # Simulate Poisson process
    events, events_time = generate_poisson_events(N, lambd)

    # Calculate histogram
    num_bins = 20
    bin_edges, bin_counts = calculate_histogram(events, num_bins)

    # Plot histogram
    plt.bar(bin_edges[:-1], bin_counts, width=bin_edges[1] - bin_edges[0], edgecolor='black')

    # Overlay a line with theoretical values
    x_values = np.arange(np.min(bin_edges), np.max(bin_edges), 0.1)
    #theoretical_values = N * (poisson.rvs(x_values, lambd))
    #plt.plot(x_values, theoretical_values, color='red', linestyle='--', label='Theoretical Values')

    plt.title('Histogram of Event Times')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

