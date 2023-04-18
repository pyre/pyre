// -*- coding: utf-8 -*-
//

#include "benchmark_kernel.h"

void
wrapInvariants(
    int nBlocks, int nThreadPerBlock, double * A, double * I1, double * I2, double * I3, int size)
{
    // Execute the kernel
    computeInvariants<<<nBlocks, nThreadPerBlock>>>(A, I1, I2, I3, size);

    return;
}

void
wrapI1(int nBlocks, int nThreadPerBlock, cudaStream_t stream, double * A, double * I1, int size)
{
    // Execute the kernel
    computeI1<<<nBlocks, nThreadPerBlock, 0, stream>>>(A, I1, size);

    return;
}

void
wrapI2(int nBlocks, int nThreadPerBlock, cudaStream_t stream, double * A, double * I2, int size)
{
    // Execute the kernel
    computeI2<<<nBlocks, nThreadPerBlock, 0, stream>>>(A, I2, size);

    return;
}
void
wrapI3(int nBlocks, int nThreadPerBlock, cudaStream_t stream, double * A, double * I3, int size)
{
    // Execute the kernel
    computeI3<<<nBlocks, nThreadPerBlock, 0 stream>>>(A, I3, size);

    return;
}

__global__ void
computeInvariants(double * A, double * I1, double * I2, double * I3, int size)
{
    // Get the index of each thread
    int index = threadIdx.x + blockDim.x * blockIdx.x;

    // Make sure that the thread fits in the dimension
    if (index < size) {
        // Compute the first invariant
        double I1[index] = A[index] + A[index + 4 * size] + A[index + 8 * size];

        // Compute the second invariant
        double I2[index] =
            A[index] * A[index + 4 * size] + A[index + 4 * size] * A[index + 8 * size]
            + A[index] * A[index + 8 * size] - A[index + size] * A[index + 3 * size]
            - A[index + 2 * size] * A[index + 6 * size] - A[index + 5 * size] * A[index + 7 * size];

        // Compute the third invariant
        double I3[index] = A[index]
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

__global__ void
computeI1(double * A, double * I1, int size)
{
    // Get the index of each thread
    int index = threadIdx.x + blockDim.x * blockIdx.x;

    // Make sure that the thread fits in the dimension
    if (index < size) {
        // Compute the first invariant
        double I1[index] = A[index] + A[index + 4 * size] + A[index + 8 * size];
    }

    return;
}

__global__ void
computeI2(double * A, double * I2, int size)
{
    // Get the index of each thread
    int index = threadIdx.x + blockDim.x * blockIdx.x;

    // Make sure that the thread fits in the dimension
    if (index < size) {
        // Compute the second invariant
        double I2[index] =
            A[index] * A[index + 4 * size] + A[index + 4 * size] * A[index + 8 * size]
            + A[index] * A[index + 8 * size] - A[index + size] * A[index + 3 * size]
            - A[index + 2 * size] * A[index + 6 * size] - A[index + 5 * size] * A[index + 7 * size];
    }

    return;
}

__global__ void
computeI3(double * A, double * I3, int size)
{
    // Get the index of each thread
    int index = threadIdx.x + blockDim.x * blockIdx.x;

    // Make sure that the thread fits in the dimension
    if (index < size) {
        // Compute the third invariant
        double I3[index] = A[index]
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