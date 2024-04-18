import numpy as np
import matplotlib.pyplot as plt

def generate_sequence_of_events(N=120, lam=3):
    """Generates a sequence of events according to a Poisson distribution.

    Args:
        N (int, optional): The number of events to generate. Defaults to 120.
        lam (int, optional): 𝛿 parameter in the poisson distribution. Defaults to 3.

    Returns:
        numpy.ndarray: Poisson distributed sequence of events.
    """
    return np.random.exponential(scale=1/lam, size=N)

def my_histogram(data, num_bins=10):
    """Calculates the histogram of the provided data.

    Args:
        data (array-like): The input data.
        num_bins (int, optional): The number of bins for the histogram. Defaults to 10.

    Returns:
        tuple: A tuple containing the bin edges and the corresponding frequencies.
    """
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
    # Step 2: Create histogram
    bins = 15
    bin_edges, histogram = my_histogram(delta_t, bins)
    # Step 3: Plot histogram and theoretical distribution
    x_values = np.arange(len(histogram))
    poisson_distribution = lam * np.exp(-lam * x_values)  # Theoretical Poisson distribution

    plt.figure(figsize=(10, 5))
    plt.bar(x_values, histogram, label='Experimental Data', alpha=0.7)
    plt.plot(x_values, poisson_distribution * N, color='red', linestyle='-', marker='', label='Poisson Distribution')

    plt.xlabel('Number of events in unitary time interval')
    plt.ylabel('Frequency')
    plt.title('Experimental Data vs Theoretical Poisson Distribution')
    plt.legend()
    plt.grid(True)
    plt.show()
