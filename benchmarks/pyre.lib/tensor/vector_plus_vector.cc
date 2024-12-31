// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved
//


// get the benchmark library
#include <benchmark/benchmark.h>

// get array
#include <array>
// get tensor
#include <pyre/tensor.h>


auto
sum_tensor(const auto & vector_1, const auto & vector_2)
{
    // return the sum of the two vectors
    return vector_1 + vector_2;
}

auto
sum_array(const auto & vector_1, const auto & vector_2)
{
    // compute the sum of the two vectors
    auto result = std::array<double, 3> { 0.0, 0.0, 0.0 };
    for (size_t i = 0; i < result.size(); ++i) {
        result[i] += vector_1[i] + vector_2[i];
    }

    // return the result
    return result;
}

static void
VectorSumArray(benchmark::State & state)
{
    // build the vectors
    auto vector_1 = std::array<double, 3> { 1.0, -1.0, 2.0 };
    auto vector_2 = std::array<double, 3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(sum_array(vector_1, vector_2));
    }
}

static void
VectorSumTensor(benchmark::State & state)
{
    // build the vectors
    auto vector_1 = pyre::tensor::vector_t<3> { 1.0, -1.0, 2.0 };
    auto vector_2 = pyre::tensor::vector_t<3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(sum_tensor(vector_1, vector_2));
    }
}


// run benchmark for 3D vector (array)
BENCHMARK(VectorSumArray);
// run benchmark for 3D vector (tensor)
BENCHMARK(VectorSumTensor);


// run all benchmarks
BENCHMARK_MAIN();


// end of file
