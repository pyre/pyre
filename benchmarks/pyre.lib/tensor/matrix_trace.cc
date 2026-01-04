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
trace_tensor(const auto & matrix)
{
    // return the trace of the matrix
    return pyre::tensor::trace(matrix);
}

auto
trace_array(const auto & matrix)
{
    // return the trace of the matrix
    return matrix[0] + matrix[4] + matrix[8];
}

static void
MatrixTraceArray(benchmark::State & state)
{
    // build the matrices
    auto matrix = std::array<double, 9> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(trace_array(matrix));
    }
}

static void
MatrixTraceTensor(benchmark::State & state)
{
    // build the matrices
    auto matrix = pyre::tensor::matrix_t<3> { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };

    // repeat the operation sufficient number of times
    for (auto _ : state) {
        benchmark::DoNotOptimize(trace_tensor(matrix));
    }
}


// run benchmark for 3D matrix (array)
BENCHMARK(MatrixTraceArray);
// run benchmark for 3D matrix (tensor)
BENCHMARK(MatrixTraceTensor);


// run all benchmarks
BENCHMARK_MAIN();


// end of file
