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
norm_3D_array(const auto & matrix)
{
    // return the norm of the matrix
    return std::sqrt(
        matrix[0] * matrix[0] + matrix[1] * matrix[1] + matrix[2] * matrix[2]
        + matrix[3] * matrix[3] + matrix[4] * matrix[4] + matrix[5] * matrix[5]
        + matrix[6] * matrix[6] + matrix[7] * matrix[7] + matrix[8] * matrix[8]);
}

auto
norm_3D_symmetric_array(const auto & matrix)
{
    // return the norm of the matrix
    return std::sqrt(
        matrix[0] * matrix[0] + 2.0 * matrix[1] * matrix[1] + 2.0 * matrix[2] * matrix[2]
        + 2.0 * matrix[3] * matrix[3] + matrix[4] * matrix[4]);
}

auto
norm_9D_diagonal_array(const auto & matrix)
{
    // return the norm of the matrix
    return std::sqrt(
        matrix[0] * matrix[0] + matrix[1] * matrix[1] + matrix[2] * matrix[2]
        + matrix[3] * matrix[3] + matrix[4] * matrix[4] + matrix[5] * matrix[5]
        + matrix[6] * matrix[6] + matrix[7] * matrix[7] + matrix[8] * matrix[8]);
}

auto
norm_tensor(const auto & matrix)
{
    // return the norm of the matrix
    return pyre::tensor::norm(matrix);
}

static void
Norm3DArray(benchmark::State & state)
{
    // build the matrix
    auto matrix = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(norm_3D_array(matrix));
    }
}

static void
Norm3DTensor(benchmark::State & state)
{
    // build the matrix
    auto matrix = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(norm_tensor(matrix));
    }
}

static void
Norm3DSymmetricArray(benchmark::State & state)
{
    // build the matrix
    auto matrix = std::array<double, 6> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(norm_3D_symmetric_array(matrix));
    }
}

static void
Norm3DSymmetricTensor(benchmark::State & state)
{
    // build the matrix
    auto matrix = pyre::tensor::symmetric_matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(norm_tensor(matrix));
    }
}

static void
Norm9DDiagonalArray(benchmark::State & state)
{
    // build the matrix
    auto matrix = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(norm_9D_diagonal_array(matrix));
    }
}

static void
Norm9DDiagonalTensor(benchmark::State & state)
{
    // build the matrix
    auto matrix =
        pyre::tensor::diagonal_matrix_t<9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(norm_tensor(matrix));
    }
}


// run benchmark for 3D matrix (array)
BENCHMARK(Norm3DArray);
// run benchmark for 3D matrix (tensor)
BENCHMARK(Norm3DTensor);
// run benchmark for 3D symmetric matrix (array)
BENCHMARK(Norm3DSymmetricArray);
// run benchmark for 3D symmetric matrix (tensor)
BENCHMARK(Norm3DSymmetricTensor);
// run benchmark for 9D diagonal matrix (array)
BENCHMARK(Norm9DDiagonalArray);
// run benchmark for 9D diagonal matrix (tensor)
BENCHMARK(Norm9DDiagonalTensor);


// run all benchmarks
BENCHMARK_MAIN();


// end of file
