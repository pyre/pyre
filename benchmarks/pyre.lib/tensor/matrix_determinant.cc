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
determinant_2D_array(const auto & matrix)
{
    // return the determinant
    return matrix[0] * matrix[3] - matrix[1] * matrix[2];
}

auto
determinant_3D_array(const auto & matrix)
{
    // return the determinant
    return matrix[0] * (matrix[4] * matrix[8] - matrix[5] * matrix[7])
         - matrix[1] * (matrix[3] * matrix[8] - matrix[5] * matrix[6])
         + matrix[2] * (matrix[3] * matrix[7] - matrix[4] * matrix[6]);
}

auto
determinant_3D_diagonal_array(const auto & matrix)
{
    // return the determinant
    return matrix[0] * matrix[1] * matrix[2];
}

auto
determinant_3D_symmetric_array(const auto & matrix)
{
    // return the determinant
    return matrix[0] * (matrix[3] * matrix[5] - matrix[4] * matrix[4])
         - matrix[1] * (matrix[1] * matrix[5] - matrix[4] * matrix[2])
         + matrix[2] * (matrix[1] * matrix[4] - matrix[3] * matrix[2]);
}

auto
determinant_tensor(const auto & matrix)
{
    // return the determinant
    return pyre::tensor::determinant(matrix);
}

static void
Determinant2DArray(benchmark::State & state)
{
    // build the matrix
    auto matrix = std::array<double, 4> { 1.0, -1.0, 2.0, 1.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(determinant_2D_array(matrix));
    }
}

static void
Determinant2DTensor(benchmark::State & state)
{
    // build the matrix
    auto matrix = pyre::tensor::matrix_t<2> { 1.0, -1.0, 2.0, 1.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(determinant_tensor(matrix));
    }
}

static void
Determinant3DArray(benchmark::State & state)
{
    // build the matrix
    auto matrix = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(determinant_3D_array(matrix));
    }
}

static void
Determinant3DTensor(benchmark::State & state)
{
    // build the matrix
    auto matrix = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(determinant_tensor(matrix));
    }
}

static void
Determinant3DSymmetricArray(benchmark::State & state)
{
    // build the matrix
    auto matrix = std::array<double, 6> { 1.0,
                                          -1.0,
                                          2.0,
                                          /*-1.0,*/ 1.0,
                                          0.0,
                                          /*2.0, 0.0,*/ 1.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(determinant_3D_symmetric_array(matrix));
    }
}

static void
Determinant3DSymmetricTensor(benchmark::State & state)
{
    // build the matrix
    auto matrix = pyre::tensor::symmetric_matrix_t<3> { 1.0,
                                                        -1.0,
                                                        2.0,
                                                        /*-1.0,*/ 1.0,
                                                        0.0,
                                                        /*2.0, 0.0,*/ 1.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(determinant_tensor(matrix));
    }
}

static void
Determinant3DDiagonalArray(benchmark::State & state)
{
    // build the matrix
    auto matrix = std::array<double, 3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(determinant_3D_diagonal_array(matrix));
    }
}

static void
Determinant3DDiagonalTensor(benchmark::State & state)
{
    // build the matrix
    auto matrix = pyre::tensor::diagonal_matrix_t<3> { 1.0, -1.0, 2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(determinant_tensor(matrix));
    }
}


// run benchmark for 2D matrix (array)
BENCHMARK(Determinant2DArray);
// run benchmark for 2D matrix (tensor)
BENCHMARK(Determinant2DTensor);
// run benchmark for 3D matrix (array)
BENCHMARK(Determinant3DArray);
// run benchmark for 3D matrix (tensor)
BENCHMARK(Determinant3DTensor);
// run benchmark for 3D symmetric matrix (array)
BENCHMARK(Determinant3DSymmetricArray);
// run benchmark for 3D symmetric matrix (tensor)
BENCHMARK(Determinant3DSymmetricTensor);
// run benchmark for 3D diagonal matrix (array)
BENCHMARK(Determinant3DDiagonalArray);
// run benchmark for 3D diagonal matrix (tensor)
BENCHMARK(Determinant3DDiagonalTensor);


// run all benchmarks
BENCHMARK_MAIN();


// end of file
