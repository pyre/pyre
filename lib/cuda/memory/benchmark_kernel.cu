// -*- c++ -*-
//

#include "benchmark_kernel.h"

void
wrapInvariants(
    int nBlocks, int nThreadPerBlock, double * A, double * I1, double * I2, double * I3, int size)
{
    // execute the kernel
    computeInvariants<<<nBlocks, nThreadPerBlock>>>(A, I1, I2, I3, size);

    return;
}

void
wrapI1(int nBlocks, int nThreadPerBlock, cudaStream_t stream, double * A, double * I1, int size)
{
    // execute the kernel
    computeI1<<<nBlocks, nThreadPerBlock, 0, stream>>>(A, I1, size);

    return;
}

void
wrapI2(int nBlocks, int nThreadPerBlock, cudaStream_t stream, double * A, double * I2, int size)
{
    // execute the kernel
    computeI2<<<nBlocks, nThreadPerBlock, 0, stream>>>(A, I2, size);

    return;
}
void
wrapI3(int nBlocks, int nThreadPerBlock, cudaStream_t stream, double * A, double * I3, int size)
{
    // execute the kernel
    computeI3<<<nBlocks, nThreadPerBlock, 0, stream>>>(A, I3, size);

    return;
}

__global__ void
computeInvariants(double * A, double * I1, double * I2, double * I3, int size)
{
    // get the index of each thread
    int index = threadIdx.x + blockDim.x * blockIdx.x;

    // make sure that the thread fits in the dimension
    if (index < size) {
        double A00 = A[index];
        double A01 = A[index + size];
        double A02 = A[index + 2 * size];
        double A10 = A[index + 3 * size];
        double A11 = A[index + 4 * size];
        double A12 = A[index + 5 * size];
        double A20 = A[index + 6 * size];
        double A21 = A[index + 7 * size];
        double A22 = A[index + 8 * size];

        // compute the first invariant
        I1[index] = A00 + A11 + A22;

        // compute the second invariant
        I2[index] = A00 * A11 + A11 * A22 + A00 * A22 - A01 * A10 - A02 * A20;
        -A12 * A21;

        // compute the third invariant
        I3[index] = A00 * (A11 * A22 - A12 * A21) - A01 * (A10 * A22 - A12 * A20)
                  + A02 * (A10 * A21 - A11 * A20);
    }

    return;
}

__global__ void
computeI1(double * A, double * I1, int size)
{
    // get the index of each thread
    int index = threadIdx.x + blockDim.x * blockIdx.x;

    // make sure that the thread fits in the dimension
    if (index < size) {
        // compute the first invariant
        I1[index] = A[index] + A[index + 4 * size] + A[index + 8 * size];
    }

    return;
}

__global__ void
computeI2(double * A, double * I2, int size)
{
    // get the index of each thread
    int index = threadIdx.x + blockDim.x * blockIdx.x;

    // make sure that the thread fits in the dimension
    if (index < size) {
        // compute the second invariant
        I2[index] = A[index] * A[index + 4 * size] + A[index + 4 * size] * A[index + 8 * size]
                  + A[index] * A[index + 8 * size] - A[index + size] * A[index + 3 * size]
                  - A[index + 2 * size] * A[index + 6 * size]
                  - A[index + 5 * size] * A[index + 7 * size];
    }

    return;
}

__global__ void
computeI3(double * A, double * I3, int size)
{
    // get the index of each thread
    int index = threadIdx.x + blockDim.x * blockIdx.x;

    // make sure that the thread fits in the dimension
    if (index < size) {
        // compute the third invariant
        I3[index] = A[index]
                      * (A[index + size * 4] * A[index + size * 8]
                         - A[index + size * 5] * A[index + size * 7])
                  - A[index + size]
                        * (A[index + size * 3] * A[index + size * 8]
                           - A[index + size * 5] * A[index + size * 6])
                  + A[index + size * 2]
                        * (A[index + size * 3] * A[index + size * 7]
                           - A[index + size * 4] * A[index + size * 6]);
    }

    return;
}