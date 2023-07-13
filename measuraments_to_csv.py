#!/usr/bin/python

import sys
import csv

def read_measurements(filename):
    measurements = []
    with open(filename) as file:
        for line in file:
            measurement = line.strip().rstrip('s')
            measurements.append(float(measurement))
    return measurements

array_size = ["32", "64", "128", "256", "512", "1024", "2048", "4096"]
impl = ["seq", "pth", "omp"]
num_threads = ["1", "2", "4", "8", "16", "32"]

# Create the CSV file
csv_filename = 'csv/measurements.csv'
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    header = ['Implementation', 'Array Size', 'Num Threads', 'Measurement']
    writer.writerow(header)

    # Write measurements for each scenario
    for i in impl:
        if i == 'seq':
            for j in array_size:
                measurements = read_measurements(f'data/{i}-{j}')
                for measurement in measurements:
                    row = [i, j, '', measurement]
                    writer.writerow(row)
        else:
            for j in array_size:
                for k in num_threads:
                    measurements = read_measurements(f'data/{i}-{j}-{k}')
                    for measurement in measurements:
                        row = [i, j, k, measurement]
                        writer.writerow(row)
