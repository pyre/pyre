// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2026 all rights reserved
//


// get the benchmark library
#include <benchmark/benchmark.h>

// get array
#include <array>
// get tensor
#include <pyre/tensor.h>


auto
norm_tensor(const auto & vector)
{
    // return the norm of the vector
    return pyre::tensor::norm(vector);
}

auto
norm_array(const auto & vector)
{
    // compute the norm of the vector
    double squared_sum = 0.;
    for (size_t i = 0; i < vector.size(); ++i) {
        squared_sum += vector[i] * vector[i];
    }

    // return the norm of the vector
    return std::sqrt(squared_sum);
}

static void
VectorNormArray(benchmark::State & state)
{
    // build the vector
    auto vector = std::array<double, 3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(norm_array(vector));
    }
}

static void
VectorNormTensor(benchmark::State & state)
{
    // build the vector
    auto vector = pyre::tensor::vector_t<3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(norm_tensor(vector));
    }
}

// run benchmark for 3D vector (array)
BENCHMARK(VectorNormArray);
// run benchmark for 3D vector (tensor)
BENCHMARK(VectorNormTensor);


// run all benchmarks
BENCHMARK_MAIN();


// end of file
