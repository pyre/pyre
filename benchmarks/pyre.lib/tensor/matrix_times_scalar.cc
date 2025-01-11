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
multiply_tensor(const auto & matrix, const auto & scalar)
{
    // return the multiplication
    return scalar * matrix;
}

auto
multiply_array(const auto & matrix, const auto & scalar)
{
    // multiply the matrix by the scalar
    auto result = std::array<double, 9> { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };
    for (size_t i = 0; i < matrix.size(); ++i) {
        result[i] = matrix[i] * scalar;
    }

    // return the result
    return result;
}

static void
MatrixTimesScalarArray(benchmark::State & state)
{
    // build the matrices
    auto matrix = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(multiply_array(matrix, std::sqrt(2.0)));
    }
}

static void
MatrixTimesScalarTensor(benchmark::State & state)
{
    // build the matrices
    auto matrix = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(multiply_tensor(matrix, std::sqrt(2.0)));
    }
}


// run benchmark for 3D matrices (array)
BENCHMARK(MatrixTimesScalarArray);
// run benchmark for 3D matrices (tensor)
BENCHMARK(MatrixTimesScalarTensor);


// run all benchmarks
BENCHMARK_MAIN();


// end of file
