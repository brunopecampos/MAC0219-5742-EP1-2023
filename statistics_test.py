import sys
import math
import matplotlib.pyplot as plt

def calculate_average(measurements):
    return sum(measurements) / len(measurements)

def calculate_confidence_interval(measurements, average, confidence_level):
    n = len(measurements)
    standard_deviation = math.sqrt(sum((x - average) ** 2 for x in measurements) / (n - 1))
    margin = standard_deviation * (1.96 / math.sqrt(n))
    return margin

array_size = ["32", "64", "128", "256", "512", "1024", "2048", "4096"]
impl = ["pth", "omp"]
num_threads = ["1", "2", "4", "8", "16", "32"]

for j in array_size:
    sequential_times = []
    pthreads_times = []
    openmp_times = []
    thread_counts = []

    for k in num_threads:
        # Read measurements from file
        sequential_measurements = []
        pthreads_measurements = []
        openmp_measurements = []

        # Read sequential measurements
        input_file = f'seq-{j}'
        with open(f'data/{input_file}') as file:
            for line in file:
                measurement = line.strip().rstrip('s')
                sequential_measurements.append(float(measurement))

        # Read pthreads measurements
        input_file = f'pth-{j}-{k}'
        with open(f'data/{input_file}') as file:
            for line in file:
                measurement = line.strip().rstrip('s')
                pthreads_measurements.append(float(measurement))

        # Read OpenMP measurements
        input_file = f'omp-{j}-{k}'
        with open(f'data/{input_file}') as file:
            for line in file:
                measurement = line.strip().rstrip('s')
                openmp_measurements.append(float(measurement))

        # Calculate average and confidence interval
        sequential_average = calculate_average(sequential_measurements)
        pthreads_average = calculate_average(pthreads_measurements)
        openmp_average = calculate_average(openmp_measurements)
        confidence_level = 0.95
        sequential_margin = calculate_confidence_interval(sequential_measurements, sequential_average, confidence_level)
        pthreads_margin = calculate_confidence_interval(pthreads_measurements, pthreads_average, confidence_level)
        openmp_margin = calculate_confidence_interval(openmp_measurements, openmp_average, confidence_level)

        # Store average times and thread counts
        sequential_times.append(sequential_average)
        pthreads_times.append(pthreads_average)
        openmp_times.append(openmp_average)
        thread_counts.append(int(k))

    # Create graph
    plt.figure()
    plt.plot(thread_counts, sequential_times, label='Sequential')
    plt.plot(thread_counts, pthreads_times, label='Pthreads')
    plt.plot(thread_counts, openmp_times, label='OpenMP')
    plt.title(f'Variação do tempo em função do número de threads para grid_size = {j}')
    plt.xlabel('Número de threads')
    plt.ylabel('Tempo (s)')
    plt.legend()
    plt.savefig(f'graph_{j}.png')
    plt.close()