#!/bin/bash

# Define the arrays
num_threads=("1" "2" "4" "8" "16" "32")
array_size=("32" "64" "128" "256" "512" "1024" "2048" "4096")
impl=("pth" "omp")

for array in "${array_size[@]}"; do
	for threads in "${num_threads[@]}"; do
        for im in "${impl[@]}"; do
            for ((i=1; i<=10; i++)); do
                ./time_test --grid_size $array --impl $im --num_threads $threads >> ../data/$im-$array-$threads
            done
        done
    done
done

impl2=("seq")

for array in "${array_size[@]}"; do
    for im in "${impl[@]}"; do
        for ((i=1; i<=10; i++)); do
            ./time_test --grid_size $array --impl $im --num_threads $threads >> ../data/$im-$array
        done
    done
done