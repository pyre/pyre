// -*- c++ -*-
//
// sebastiaan van paasen
// (c) 1998-2023 all rights reserved

// get the journal
#include <pyre/journal.h>
// add the grid
#include <pyre/grid.h>
// add the cuda memory
#include <pyre/cuda/memory.h>
// and the timers
#include <pyre/timers.h>

// type alias
using canonical_t = pyre::grid::canonical_t<2>;
using pack_t = pyre::grid::canonical_t<2>;

// memory storage
using managed_storage_t = pyre::cuda::memory::managed_t<double>;
using pinned_storage_t = pyre::cuda::memory::pinned_t<double>;
using mapped_storage_t = pyre::cuda::memory::mapped_t<double>;

// grids
using grid_managed_t = pyre::grid::grid_t<pack_t, managed_storage_t>;
using grid_pinned_t = pyre::grid::grid_t<pack_t, pinned_storage_t>;
using grid_mapped_t = pyre::grid::grid_t<pack_t, mapped_storage_t>;

// timer
using proctimer_t = pyre::timers::process_timer_t;
using walltimer_t = pyre::timers::wall_timer_t;

void
computeInvariantsManaged(
    int nTensors, int nThreadPerBlock, int nBlocks, const double * tensorArray,
    double * inverseArray);

void
computeInvariantsPinned(
    int nTensors, int nThreadPerBlock, int nBlocks, double * gpuTensors, double * gpuInverses);

void
computeInvariantsMapped(
    int nTensors, int nThreadPerBlock, int nBlocks, const double * tensorArray,
    double * inverseArray);

void
managedInverses(pack_t tensorPack, int nThreadPerBlock, int nTensors)
{
    // and assemble in a grid
    grid_managed_t tensorArray { tensorPack, tensorPack.cells() };
    grid_managed_t inverseArray { tensorPack, tensorPack.cells() };

    // create an array of arrays as pertubation of identity
    double perturbation = 0.1;
    int i, j, ij, jj;
    for (int nTensor = 0; nTensor < nTensors; nTensor++) {
        for (j = 0, ij = 0, jj = 0; j < 3; j++, jj += 4) {
            for (i = 0; i < 3; i++, ij++) {
                // Get the current index
                canonical_t::index_type index { ij, nTensor };
                // std::cout << "\nTesting index cpu: " << index << std::endl;
                // Compute the random perturbations
                tensorArray.at(index) = perturbation * (2 * (double) rand() / RAND_MAX - 1.0);
            }

            // Get the current index
            canonical_t::index_type index { jj, nTensor };
            tensorArray.at(index) += 1.0;
        }
    }

    // setup the grid for the gpu computation
    int nBlocks;

    // check if multiple blocks are necessary
    if (nTensors > nThreadPerBlock) {
        // allocate possibly too many workers
        nBlocks = nTensors / nThreadPerBlock + 1;

        // so check how many are in the last block
        int nThreadLastBlock = nTensors - (nBlocks - 1) * nThreadPerBlock;

        // and remove the block if it is not used
        if (nThreadLastBlock == 0) {
            nBlocks -= 1;
        }
    } else {
        // if one block is enough
        nThreadPerBlock = nTensors;
        // allocate only one block
        nBlocks = 1;
    }

    // make sure the GPU is available before starting the timer
    cudaError_t status = cudaDeviceSynchronize();
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("pyre.cuda");
        // complain
        error << "while synchronizing the GPU " << pyre::journal::newline
              << cudaGetErrorName(status) << " (" << status << ")" << pyre::journal::endl(__HERE__);
        // and bail
        throw std::bad_alloc();
    }

    // make a general timer
    proctimer_t timer("tests.timer");

    // make a wallclock timer
    walltimer_t walltimer("tests.timer");

    // reset the general timer
    timer.reset();

    // start the timer
    timer.start();

    // start the wallclock timer
    walltimer.start();

    // execute the kernel wrapper
    computeInvariantsManaged(
        nTensors, nThreadPerBlock, nBlocks, tensorArray.data()->data(),
        inverseArray.data()->data());

    // wait for GPU to finish before stopping the timer
    status = cudaDeviceSynchronize();
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("pyre.cuda");
        // complain
        error << "while synchronizing the GPU " << pyre::journal::newline
              << cudaGetErrorName(status) << " (" << status << ")" << pyre::journal::endl(__HERE__);
        // and bail
        throw std::bad_alloc();
    }

    // stop the general timer
    timer.stop();

    // and stop the wallclock timer
    walltimer.stop();

    // make a channel
    pyre::journal::debug_t timerChannel("tests.timer");
    // activate it
    timerChannel.activate();
    // show me
    timerChannel
        // show me the elapsed time
        << "Managed memory tensor inverse computation: " << pyre::journal::newline
        << pyre::journal::indent(1) << "General timer time:  " << timer.ms() << " ms"
        << pyre::journal::newline << pyre::journal::indent(1)
        << "Wallclock time: " << walltimer.ms() << " ms" << pyre::journal::outdent(1)
        << pyre::journal::endl(__HERE__);

    // all done
    return;
}


void
pinnedInverses(pack_t tensorPack, int nThreadPerBlock, int nTensors)
{
    // assemble in a grid
    grid_pinned_t tensorArray { tensorPack, tensorPack.cells() };
    grid_pinned_t inverseArray { tensorPack, tensorPack.cells() };

    // create an array of arrays as pertubation of identity
    double perturbation = 0.1;
    int i, j, ij, jj;
    for (int nTensor = 0; nTensor < nTensors; nTensor++) {
        for (j = 0, ij = 0, jj = 0; j < 3; j++, jj += 4) {
            for (i = 0; i < 3; i++, ij++) {
                // Get the current index
                canonical_t::index_type index { ij, nTensor };
                // Compute the random perturbations
                tensorArray.at(index) = perturbation * (2 * (double) rand() / RAND_MAX - 1.0);
            }

            // Get the current index
            canonical_t::index_type index { jj, nTensor };
            tensorArray.at(index) += 1.0;
        }
    }

    // and the gpu memory
    double *gpuTensors, *gpuInverses;
    auto status = cudaMalloc(&gpuTensors, nTensors * 9 * sizeof(double));
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("pyre.cuda");
        // complain
        error << "while allocating " << nTensors * 9
              << " bytes of device memory: " << pyre::journal::newline << cudaGetErrorName(status)
              << " (" << status << ")" << pyre::journal::endl(__HERE__);
        // and bail
        throw std::bad_alloc();
    }

    status = cudaMalloc(&gpuInverses, nTensors * 9 * sizeof(double));
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("pyre.cuda");
        // complain
        error << "while allocating " << nTensors * 9
              << " bytes of device memory: " << pyre::journal::newline << cudaGetErrorName(status)
              << " (" << status << ")" << pyre::journal::endl(__HERE__);
        // and bail
        throw std::bad_alloc();
    }

    // setup the grid for the gpu computation
    int nBlocks;

    // check if multiple blocks are necessary
    if (nTensors > nThreadPerBlock) {
        // allocate possibly too many workers
        nBlocks = nTensors / nThreadPerBlock + 1;

        // so check how many are in the last block
        int nThreadLastBlock = nTensors - (nBlocks - 1) * nThreadPerBlock;

        // and remove the block if it is not used
        if (nThreadLastBlock == 0) {
            nBlocks -= 1;
        }
    } else {
        // if one block is enough
        nThreadPerBlock = nTensors;
        // allocate only one block
        nBlocks = 1;
    }

    // make sure the GPU is available before starting the timer
    status = cudaDeviceSynchronize();
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("pyre.cuda");
        // complain
        error << "while synchronizing the GPU " << pyre::journal::newline
              << cudaGetErrorName(status) << " (" << status << ")" << pyre::journal::endl(__HERE__);
        // and bail
        throw std::bad_alloc();
    }

    // make a general timer
    proctimer_t timer("tests.timer");

    // make a wallclock timer
    walltimer_t walltimer("tests.timer");

    // reset the general timer
    timer.reset();

    // start the timer
    timer.start();

    // start the wallclock timer
    walltimer.start();

    // synchronize the tensors between host and device
    tensorArray.data()->synchronizeHostToDevice();

    // execute the kernel wrapper
    computeInvariantsPinned(
        nTensors, nThreadPerBlock, nBlocks, tensorArray.data()->device(),
        inverseArray.data()->device());

    // wait for GPU to finish before synchronizing the inverse
    status = cudaDeviceSynchronize();
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("pyre.cuda");
        // complain
        error << "while synchronizing the GPU " << pyre::journal::newline
              << cudaGetErrorName(status) << " (" << status << ")" << pyre::journal::endl(__HERE__);
        // and bail
        throw std::bad_alloc();
    }

    // and synchronize the inverse between device and host
    inverseArray.data()->synchronizeDeviceToHost();

    // wait for GPU to finish before stopping the timer
    status = cudaDeviceSynchronize();
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("pyre.cuda");
        // complain
        error << "while synchronizing the GPU " << pyre::journal::newline
              << cudaGetErrorName(status) << " (" << status << ")" << pyre::journal::endl(__HERE__);
        // and bail
        throw std::bad_alloc();
    }

    // stop the general timer
    timer.stop();

    // and stop the wallclock timer
    walltimer.stop();

    // make a channel
    pyre::journal::debug_t timerChannel("tests.timer");
    // activate it
    timerChannel.activate();
    // show me
    timerChannel
        // show me the elapsed time
        << "Pinned memory tensor inverse computation: " << pyre::journal::newline
        << pyre::journal::indent(1) << "General timer time:  " << timer.ms() << " ms"
        << pyre::journal::newline << pyre::journal::indent(1)
        << "Wallclock time: " << walltimer.ms() << " ms" << pyre::journal::outdent(1)
        << pyre::journal::endl(__HERE__);

    // all done
    return;
}

void
mappedInverses(pack_t tensorPack, int nThreadPerBlock, int nTensors)
{
    // and assemble in a grid
    grid_mapped_t tensorArray { tensorPack, tensorPack.cells() };
    grid_mapped_t inverseArray { tensorPack, tensorPack.cells() };

    // create an array of arrays as pertubation of identity
    double perturbation = 0.1;
    int i, j, ij, jj;
    for (int nTensor = 0; nTensor < nTensors; nTensor++) {
        for (j = 0, ij = 0, jj = 0; j < 3; j++, jj += 4) {
            for (i = 0; i < 3; i++, ij++) {
                // Get the current index
                canonical_t::index_type index { ij, nTensor };
                // Compute the random perturbations
                tensorArray.at(index) = perturbation * (2 * (double) rand() / RAND_MAX - 1.0);
            }

            // Get the current index
            canonical_t::index_type index { jj, nTensor };
            tensorArray.at(index) += 1.0;
        }
    }

    // setup the grid for the gpu computation
    int nBlocks;

    // check if multiple blocks are necessary
    if (nTensors > nThreadPerBlock) {
        // allocate possibly too many workers
        nBlocks = nTensors / nThreadPerBlock + 1;

        // so check how many are in the last block
        int nThreadLastBlock = nTensors - (nBlocks - 1) * nThreadPerBlock;

        // and remove the block if it is not used
        if (nThreadLastBlock == 0) {
            nBlocks -= 1;
        }
    } else {
        // if one block is enough
        nThreadPerBlock = nTensors;
        // allocate only one block
        nBlocks = 1;
    }

    // make sure the GPU is available before starting the timer
    cudaError_t status = cudaDeviceSynchronize();
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("pyre.cuda");
        // complain
        error << "while synchronizing the GPU " << pyre::journal::newline
              << cudaGetErrorName(status) << " (" << status << ")" << pyre::journal::endl(__HERE__);
        // and bail
        throw std::bad_alloc();
    }

    // make a general timer
    proctimer_t timer("tests.timer");

    // make a wallclock timer
    walltimer_t walltimer("tests.timer");

    // reset the general timer
    timer.reset();

    // start the timer
    timer.start();

    // start the wallclock timer
    walltimer.start();

    // execute the kernel wrapper
    computeInvariantsMapped(
        nTensors, nThreadPerBlock, nBlocks, tensorArray.data()->device(),
        inverseArray.data()->device());

    // wait for GPU to finish before stopping the timer
    status = cudaDeviceSynchronize();
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("pyre.cuda");
        // complain
        error << "while synchronizing the GPU " << pyre::journal::newline
              << cudaGetErrorName(status) << " (" << status << ")" << pyre::journal::endl(__HERE__);
        // and bail
        throw std::bad_alloc();
    }

    // stop the general timer
    timer.stop();

    // and stop the wallclock timer
    walltimer.stop();

    // make a channel
    pyre::journal::debug_t timerChannel("tests.timer");
    // activate it
    timerChannel.activate();
    // show me
    timerChannel
        // show me the elapsed time
        << "Mapped memory tensor inverse computation: " << pyre::journal::newline
        << pyre::journal::indent(1) << "General timer time:  " << timer.ms() << " ms"
        << pyre::journal::newline << pyre::journal::indent(1)
        << "Wallclock time: " << walltimer.ms() << " ms" << pyre::journal::outdent(1)
        << pyre::journal::endl(__HERE__);

    // all done
    return;
}

// main program
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);

    // make a channel
    pyre::journal::debug_t channel("pyre.cuda.benchmark");

    // determine the amount of tensors
    int nTensors = 34e6;

    // determine the shape
    canonical_t::shape_type tensorShape { 9, nTensors };

    // that leads to the pack
    pack_t tensorPack { tensorShape };

    // define the amount of threads per block
    int nThreadsBlock = 256;

    // test the managed memory
    managedInverses(tensorPack, nThreadsBlock, nTensors);

    // test the pinned memory
    pinnedInverses(tensorPack, nThreadsBlock, nTensors);

    // test the mapped memory
    mappedInverses(tensorPack, nThreadsBlock, nTensors);

    // all done
    return 0;
}

// end of file
