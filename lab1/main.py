import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon

def generate_sequence_of_events(N=120, lam=3):
    events = np.zeros(N)
    events_time = np.zeros(N)
    current_time = 0
    for i in range(N):
        delta_t = np.random.exponential(1 / lam)
        current_time += delta_t
        events[i] = delta_t
        events_time[i] = current_time
    return events, events_time

def my_histogram(data, num_bins=10):
    """Calculates the histogram of the provided data.

    Args:
        data (array-like): The input data.
        num_bins (int, optional): The number of bins for the histogram. Defaults to 10.

    Returns:
        tuple: A tuple containing the bin edges and the corresponding frequencies.
    """
    bin_size = (max(data) - min(data)) / num_bins
    bins = [min(data) + i * bin_size for i in range(num_bins)]
    bins.append(max(data))

    counts = [0 for _ in range(num_bins)]

    for value in data:
        for bi in range(num_bins):
            if bi == num_bins - 1 and value == bins[bi]:
                counts[bi] += 1
                break
            if bins[bi] <= value < bins[bi+1]:
                counts[bi] += 1
                break

    return bins, counts

if __name__ == '__main__':
    # Step 1: Generate sequence of events
    N = 1200
    lam = 3
    events, events_time = generate_sequence_of_events(N, lam)

    # Step 2: Create histogram
    bins = 30
    bin_edges, histogram = my_histogram(events, bins)

    # Step 3: Plot histogram
    # Plot theoretical exponential distribution

    # Generate x values for theoretical exponential distribution
    x = np.linspace(min(events), max(events), 100)
    # Calculate corresponding y values
    y = len(events) * (bin_edges[1] - bin_edges[0]) * expon.pdf(x, scale=1/lam)
    plt.plot(x, y, 'r--', label='Theoretical')

    # Experimental data
    plt.bar(bin_edges[:-1], histogram, width=(bin_edges[1]-bin_edges[0]), align='edge')
    plt.grid(True)
    plt.show()
