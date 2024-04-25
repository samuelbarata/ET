
def histogram(data):
    histogram = {}
    for value in data:
        histogram[value] = histogram.get(value, 0) + 1
    return histogram
