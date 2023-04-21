// -*- c++ -*-
//

// code guard
#if !defined(pyre_cuda_memory_benchmark_kernels_h)
#define pyre_cuda_memory_benchmark_kernels_h

#include <cuda_runtime.h>

void
wrapInvariants(
    int nBlocks, int nTheradPerBlock, double * A, double * I1, double * I2, double * I3, int size);

void
wrapI1(int nBlocks, int nThreadPerBlock, cudaStream_t stream, double * A, double * I1, int size);

void
wrapI2(int nBlocks, int nThreadPerBlock, cudaStream_t stream, double * A, double * I2, int size);

void
wrapI3(int nBlocks, int nThreadPerBlock, cudaStream_t stream, double * A, double * I3, int size);

__global__ void
computeInvariants(double * A, double * I1, double * I2, double * I3, int size);

__global__ void
computeI1(double * A, double * I1, int size);

__global__ void
computeI2(double * A, double * I2, int size);

__global__ void
computeI3(double * A, double * I3, int size);

#endif

// end of file