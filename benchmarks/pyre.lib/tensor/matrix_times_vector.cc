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
multiply_tensor(const auto & matrix, const auto & vector)
{
    // return the multiplication
    return matrix * vector;
}

auto
multiply_array(const auto & matrix, const auto & vector)
{
    // multiply the matrix by the scalar
    auto result = std::array<double, 3> { 0.0, 0.0, 0.0 };
    for (size_t i = 0; i < vector.size(); ++i) {
        for (size_t j = 0; j < vector.size(); ++j) {
            result[i] += matrix[i * 3 + j] * vector[j];
        }
    }

    // return the result
    return result;
}

static void
MatrixTimesVectorArray(benchmark::State & state)
{
    // build the matrices
    auto matrix = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto vector = std::array<double, 3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(multiply_array(matrix, vector));
    }
}

static void
MatrixTimesVectorTensor(benchmark::State & state)
{
    // build the matrices
    auto matrix = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto vector = pyre::tensor::vector_t<3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(multiply_tensor(matrix, vector));
    }
}

static void
SymmetricMatrixTimesVectorArray(benchmark::State & state)
{
    // build the matrices
    auto matrix = std::array<double, 9> { 1.0, -1.0, 2.0, -1.0, 1.0, 0.0, 2.0, 0.0, 1.0 };
    auto vector = std::array<double, 3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(multiply_array(matrix, vector));
    }
}

static void
SymmetricMatrixTimesVectorTensor(benchmark::State & state)
{
    // build the matrices
    auto matrix = pyre::tensor::symmetric_matrix_t<3> { 1.0,
                                                        -1.0,
                                                        2.0,
                                                        /*-1.0,*/ 1.0,
                                                        0.0,
                                                        /*2.0, 0.0,*/ 1.0 };
    auto vector = pyre::tensor::vector_t<3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(multiply_tensor(matrix, vector));
    }
}


// run benchmark for 3D matrices (array)
BENCHMARK(MatrixTimesVectorArray);
// run benchmark for 3D matrices (tensor)
BENCHMARK(MatrixTimesVectorTensor);
// run benchmark for 3D symmetric matrices (array)
BENCHMARK(SymmetricMatrixTimesVectorArray);
// run benchmark for 3D symmetric matrices (tensor)
BENCHMARK(SymmetricMatrixTimesVectorTensor);


// run all benchmarks
BENCHMARK_MAIN();


// end of file
