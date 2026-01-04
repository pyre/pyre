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
sum_tensor(const auto & matrix_1, const auto & matrix_2)
{
    // return the sum of the matrices
    return matrix_1 + matrix_2;
}

auto
sum_array(const auto & matrix_1, const auto & matrix_2)
{
    // add up the matrices
    auto result = std::array<double, 9> { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };
    for (size_t i = 0; i < matrix_1.size(); ++i) {
        result[i] += matrix_1[i] + matrix_2[i];
    }

    // return the result
    return result;
}

static void
MatrixPlusMatrixArray(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto matrix_2 = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(sum_array(matrix_1, matrix_2));
    }
}

static void
MatrixPlusMatrixTensor(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto matrix_2 = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(sum_tensor(matrix_1, matrix_2));
    }
}

static void
MatrixPlusSymmetricMatrixArray(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto matrix_2 = std::array<double, 9> { 1.0, -1.0, 2.0, -1.0, 1.0, 0.0, 2.0, 0.0, 1.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(sum_array(matrix_1, matrix_2));
    }
}

static void
MatrixPlusSymmetricMatrixTensor(benchmark::State & state)
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
        benchmark::DoNotOptimize(sum_tensor(matrix_1, matrix_2));
    }
}

static void
MatrixPlusDiagonalMatrixArray(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto matrix_2 = std::array<double, 9> { 1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(sum_array(matrix_1, matrix_2));
    }
}

static void
MatrixPlusDiagonalMatrixTensor(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    auto matrix_2 = pyre::tensor::diagonal_matrix_t<3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(sum_tensor(matrix_1, matrix_2));
    }
}

static void
SymmetricMatrixPlusDiagonalMatrixArray(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = std::array<double, 9> { 1.0, -1.0, 2.0, -1.0, 1.0, 0.0, 2.0, 0.0, 1.0 };
    auto matrix_2 = std::array<double, 9> { 1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(sum_array(matrix_1, matrix_2));
    }
}

static void
SymmetricMatrixPlusDiagonalMatrixTensor(benchmark::State & state)
{
    // build the matrices
    auto matrix_1 = pyre::tensor::symmetric_matrix_t<3> { 1.0,
                                                          -1.0,
                                                          2.0,
                                                          /*-1.0,*/ 1.0,
                                                          0.0,
                                                          /*2.0, 0.0,*/ 1.0 };
    auto matrix_2 = pyre::tensor::diagonal_matrix_t<3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(sum_tensor(matrix_1, matrix_2));
    }
}


// run benchmark for 3D matrices (array)
BENCHMARK(MatrixPlusMatrixArray);
// run benchmark for 3D matrices (tensor)
BENCHMARK(MatrixPlusMatrixTensor);
// run benchmark for 3D matrix and symmetric matrix (array)
BENCHMARK(MatrixPlusSymmetricMatrixArray);
// run benchmark for 3D matrix and symmetric matrix (tensor)
BENCHMARK(MatrixPlusSymmetricMatrixTensor);
// run benchmark for 3D matrix and diagonal matrix (array)
BENCHMARK(MatrixPlusDiagonalMatrixArray);
// run benchmark for 3D matrix diagonal matrix (tensor)
BENCHMARK(MatrixPlusDiagonalMatrixTensor);
// run benchmark for 3D diagonal matrix and symmetric matrix (array)
BENCHMARK(SymmetricMatrixPlusDiagonalMatrixArray);
// run benchmark for 3D diagonal matrix and symmetric matrix (tensor)
BENCHMARK(SymmetricMatrixPlusDiagonalMatrixTensor);


// run all benchmarks
BENCHMARK_MAIN();


// end of file
