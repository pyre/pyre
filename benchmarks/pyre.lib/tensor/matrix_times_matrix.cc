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
multiply_tensor(const auto & matrix_1, const auto & matrix_2)
{
    // return the multiplication of the matrices
    return matrix_1 * matrix_2;
}

auto
multiply_array(const auto & matrix_1, const auto & matrix_2)
{
    // multiply the matrices
    auto result = std::array<double, 9> { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };
    const auto dim = matrix_1.size() / 3;
    // matrix * matrix (array)
    for (size_t i = 0; i < dim; ++i) {
        for (size_t j = 0; j < dim; ++j) {
            for (size_t k = 0; k < dim; ++k) {
                result[j + i * dim] += matrix_1[k + i * dim] * matrix_2[j + k * dim];
            }
        }
    }

    // return the result
    return result;
}

static void
MatrixTimesMatrixArray(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto matrix_2 = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(multiply_array(matrix_1, matrix_2));
    }
}

static void
MatrixTimesMatrixTensor(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto matrix_2 = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(multiply_tensor(matrix_1, matrix_2));
    }
}

static void
MatrixTimesSymmetricMatrixArray(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto matrix_2 = std::array<double, 9> { 1.0, -1.0, 2.0, -1.0, 1.0, 0.0, 2.0, 0.0, 1.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(multiply_array(matrix_1, matrix_2));
    }
}

static void
MatrixTimesSymmetricMatrixTensor(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto matrix_2 = pyre::tensor::symmetric_matrix_t<3> { 1.0,
                                                          -1.0,
                                                          2.0,
                                                          /*-1.0,*/ 1.0,
                                                          0.0,
                                                          /*2.0, 0.0,*/ 1.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(multiply_tensor(matrix_1, matrix_2));
    }
}


// run benchmark for 3D matrices (array)
BENCHMARK(MatrixTimesMatrixArray);
// run benchmark for 3D matrices (tensor)
BENCHMARK(MatrixTimesMatrixTensor);
// run benchmark for 3D matrix and symmetric matrix (array)
BENCHMARK(MatrixTimesSymmetricMatrixArray);
// run benchmark for 3D matrix and symmetric matrix (tensor)
BENCHMARK(MatrixTimesSymmetricMatrixTensor);


// run all benchmarks
BENCHMARK_MAIN();


// end of file
