import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial

def generate_sequence_of_events(N=120, lam=3):
    """Generates a sequence of events according to a Poisson distribution.

    https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.poisson.html#numpy.random.Generator.poisson

    Args:
        N (int, optional): The number of events to generate. Defaults to 120.
        lam (int, optional): 𝛿 parameter in the poisson distribution. Defaults to 3.

    Returns:
        numpy.ndarray: Poisson distributed sequence of events.
    """
    uni = np.random.uniform(0,1, N)
    delta_t = [-np.log(1 - u) / lam for u in uni]

    # rng = np.random.default_rng()
    # return rng.poisson(lam, N)
    # return np.random.exponential(lam, size=N)
    return delta_t

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

    counts = [0 for _ in range(num_bins-1)]

    for value in data:
        for bi in range(num_bins+1):
            if bi == num_bins:
                counts[bi] += 1
                break
            if float(bins[bi]) <= value < float(bins[bi+1]):
                print(f"{type(value)}-{bins[bi]}>={value}>{bins[bi+1]}-{bi}")
                counts[bi] += 1
                break



    return bins, counts

if __name__ == '__main__':
    # Step 1: Generate sequence of events
    N = 120
    lam = 3
    delta_t = generate_sequence_of_events(N, lam)



    plt.hist(delta_t, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Time')
    plt.ylabel('Number of Events')
    plt.title('Histogram of Events Occurring in a Unitary Time Interval')
    plt.grid(True)
    plt.show()


    # Step 2: Create histogram
    bins = 30
    histogram, bin_edges = np.histogram(delta_t, bins, density=True)
    # bin_edges, histogram = my_histogram(delta_t, bins)




    # print(bin_edges)
    # print(histogram)

    # x_values = []
    # for k in range(len(bin_edges)-1):
    #     x_values.append((bin_edges[k] + bin_edges[k+1])/2.0)

    # print(bin_edges)
    # print(x_values)

    # plt.bar(x_values, histogram, label='Experimental Data')
    # plt.show()

