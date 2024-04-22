import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

def generate_poisson(N=120, lam=3):
    rng = np.random.default_rng()
    return rng.poisson(lam=lam, size=N)

def my_histogram(data, num_bins=10, inteiro=False, lam=3):
    """Calculates the histogram of the provided data.

    Args:
        data (array-like): The input data.
        num_bins (int, optional): The number of bins for the histogram. Defaults to 10.

    Returns:
        tuple: A tuple containing the bin edges and the corresponding frequencies.
    """
    if inteiro:
        bin_size = round((max(data) - min(data))/num_bins + 0.5)
        bins = [int(lam- num_bins/2*bin_size) + i*bin_size for i in range(num_bins)]
        bins.append(int(max(data)))
    else:
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

def dois_dois():
    # Step 1: Generate sequence of events
    N = 1200
    lam = 30
    events = generate_poisson(N, lam)

    # Step 2: Create histogram
    bins = 10
    bin_edges, histogram = my_histogram(events, bins, inteiro=True, lam=lam)

    # Step 3: Plot histogram
    # Plot theoretical exponential distribution

    # Generate x values for theoretical exponential distribution
    # x = np.linspace(min(events), max(events), 100)
    # Calculate corresponding y values
    x = [x for x in range(50)]
    y = len(events) * poisson.pmf(x, mu=lam, loc=0)
    plt.stem(x, y, 'r--', label='Theoretical')

    # Experimental data
    plt.bar(bin_edges[:-1], histogram, width=(bin_edges[1]-bin_edges[0]), align='edge')
    plt.grid(True)
    plt.show()

def dois_tres():
    lambdas = [3, 7, 13, 15]
    N = 1200
    events = []

    for lam in lambdas:
        new_events, events_time = generate_sequence_of_events(N, lam)
        events.extend(new_events)

    bins = 30
    bin_edges, histogram = my_histogram(events, bins)

    x = np.linspace(min(events), max(events), 100)
    y = [0 for _ in range(len(x))]
    for lam in lambdas:
        new_y = (len(events) * (bin_edges[1] - bin_edges[0]) * expon.pdf(x, scale=1/lam))
        y = [y[i] + new_y[i] for i in range(len(y))]


    plt.plot(x, y, 'r--', label='Theoretical')
    plt.bar(bin_edges[:-1], histogram, width=(bin_edges[1]-bin_edges[0]), align='edge')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    dois_dois()
