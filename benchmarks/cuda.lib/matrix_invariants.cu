// -*- c++ -*-
//
// sebastiaan van paasen
// (c) 1998-2023 all rights reserved

// function to compute the invariants of a 3x3 tensor
__global__ void
computeInvariants(const double * A, double * I1, double * I2, double * I3, int size)
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
        I2[index] = A00 * A11 + A11 * A22 + A00 * A22 - A01 * A10 - A02 * A20 - A12 * A21;

        // compute the third invariant
        I3[index] = A00 * (A11 * A22 - A12 * A21) - A01 * (A10 * A22 - A12 * A20)
                  + A02 * (A10 * A21 - A11 * A20);
    }

    return;
}

void
computeInvariantsManaged(
    int nTensors, int nThreadPerBlock, int nBlocks, const double * tensorArray, double * I1,
    double * I2, double * I3)
{
    // execute the kernel
    computeInvariants<<<nBlocks, nThreadPerBlock>>>(tensorArray, I1, I2, I3, nTensors);

    // all done
    return;
}

void
computeInvariantsPinned(
    int nTensors, int nThreadPerBlock, int nBlocks, double * gpuTensors, double * gpuI1,
    double * gpuI2, double * gpuI3)
{
    // execute the kernel
    computeInvariants<<<nBlocks, nThreadPerBlock>>>(gpuTensors, gpuI1, gpuI2, gpuI3, nTensors);

    // all done
    return;
}

void
computeInvariantsMapped(
    int nTensors, int nThreadPerBlock, int nBlocks, const double * tensorArray, double * I1,
    double * I2, double * I3)
{
    // execute the kernel
    computeInvariants<<<nBlocks, nThreadPerBlock>>>(tensorArray, I1, I2, I3, nTensors);

    // all done
    return;
}

// end of file
