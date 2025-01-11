// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved
//


// get the benchmark library
#include <benchmark/benchmark.h>

// get array
#include <array>
// get tensor
#include <pyre/tensor.h>


auto
times_tensor(const auto & vector, const auto & scalar)
{
    // return the multiplication times scalar
    return scalar * vector;
}

auto
times_array(const auto & vector, const auto & scalar)
{
    // compute the sum of the two vectors
    auto result = std::array<double, 3> { 0.0, 0.0, 0.0 };
    for (size_t i = 0; i < result.size(); ++i) {
        result[i] += scalar * vector[i];
    }

    // return the result
    return result;
}

static void
VectorTimesScalarArray(benchmark::State & state)
{
    // build the vector
    auto vector = std::array<double, 3> { 1.0, -1.0, 2.0 };
    auto scalar = std::sqrt(2);

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(times_array(vector, scalar));
    }
}

static void
VectorTimesScalarTensor(benchmark::State & state)
{
    // build the vector
    auto vector = pyre::tensor::vector_t<3> { 1.0, -1.0, 2.0 };
    auto scalar = std::sqrt(2);

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(times_tensor(vector, scalar));
    }
}


// run benchmark for 3D vector (array)
BENCHMARK(VectorTimesScalarArray);
// run benchmark for 3D vector (tensor)
BENCHMARK(VectorTimesScalarTensor);


// run all benchmarks
BENCHMARK_MAIN();


// end of file
