// -*- c++ -*-
//
// sebastiaan van paasen
// (c) 1998-2023 all rights reserved

// function to compute the invariants of a 3x3 tensor
__global__ void
computeInverse(const double * A, double * Ainv, int size)
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

        // compute the determinant of A
        double detA = A00 * (A11 * A22 - A12 * A21) - A01 * (A10 * A22 - A12 * A20)
                    + A02 * (A10 * A21 - A11 * A20);

        // set to its inverse
        double detInv = 1.0 / detA;

        // and return the inverse tensor
        Ainv[index] = detInv * (A11 * A22 - A12 * A21);
        Ainv[index + size] = detInv * (-A01 * A22 + A02 * A21);
        Ainv[index + 2 * size] = detInv * (A01 * A12 - A02 * A11);
        Ainv[index + 3 * size] = detInv * (-A10 * A22 + A12 * A20);
        Ainv[index + 4 * size] = detInv * (A00 * A22 - A02 * A20);
        Ainv[index + 5 * size] = detInv * (-A00 * A12 + A02 * A10);
        Ainv[index + 6 * size] = detInv * (A10 * A21 - A11 * A20);
        Ainv[index + 7 * size] = detInv * (-A00 * A21 + A01 * A20);
        Ainv[index + 8 * size] = detInv * (A00 * A11 - A01 * A10);
    }

    return;
}

void
computeInvariantsManaged(
    int nTensors, int nThreadPerBlock, int nBlocks, const double * tensorArray,
    double * inverseArray)
{
    // execute the kernel
    computeInverse<<<nBlocks, nThreadPerBlock>>>(tensorArray, inverseArray, nTensors);

    // all done
    return;
}


void
computeInvariantsPinned(
    int nTensors, int nThreadPerBlock, int nBlocks, double * gpuTensors, double * gpuInverses)
{
    // execute the kernel
    computeInverse<<<nBlocks, nThreadPerBlock>>>(gpuTensors, gpuInverses, nTensors);

    // all done
    return;
}

void
computeInvariantsMapped(
    int nTensors, int nThreadPerBlock, int nBlocks, const double * tensorArray,
    double * inverseArray)
{
    // execute the kernel
    computeInverse<<<nBlocks, nThreadPerBlock>>>(tensorArray, inverseArray, nTensors);

    // all done
    return;
}

// end of file
