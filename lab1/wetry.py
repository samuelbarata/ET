import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial


def generate_sequence_of_events(N=120, lam=3):
    return np.random.poisson(lam, N)
    #return np.random.exponential(scale=1/lam, size=N)

def my_histogram(data, num_bins=10):
    bin_edges = np.linspace(0, max(data), num_bins)  # Divide into bins
    counts = np.zeros(num_bins)

    for value in data:
        bin_idx = np.digitize(value, bin_edges) - 1  # Find the appropriate bin
        counts[bin_idx] += 1

    return bin_edges[:-1], counts  # Remove extra edge

if __name__ == '__main__':
    # Step 1: Generate sequence of events
    N = 120
    lam = 3
    delta_t = generate_sequence_of_events(N, lam)
    count, bins, ignored = plt.hist(delta_t, 14, density=True)
    plt.show()

    print(delta_t)
    # Step 2: Create histogram
    bins = 16
    #bin_edges, histogram = my_histogram(delta_t, bins)
    histogram, bin_edges = np.histogram(delta_t, bins)
    print(bin_edges)
    # Step 3: Plot histogram and theoretical distribution
    x_values = np.arange(len(histogram))

    #poisson_distribution = lam * np.exp(-lam * x_values)  # Theoretical Poisson distribution
    poisson_distribution = np.exp(-lam)*np.power(lam, x_values)/factorial(x_values)
    # Calculate midPoints of the bins
    pos_values = [(bin_edges[k] + bin_edges[k+1]) / 2 for k in range(len(bin_edges) - 1)]
    pos_values = []
    for k in range(len(bin_edges)-1):
        pos_values.append((bin_edges[k] + bin_edges[k+1])/2)

    plt.figure(figsize=(10, 5))
    plt.bar(x_values, histogram, label='Experimental Data', alpha=0.7)
    plt.plot(pos_values, poisson_distribution * N, color='red', linestyle='-', marker='', label='Poisson Distribution')

    plt.xlabel('Number of events in unitary time interval')
    plt.ylabel('Frequency')
    plt.title('Experimental Data vs Theoretical Poisson Distribution')
    plt.legend()
    plt.grid(True)
    plt.show()
