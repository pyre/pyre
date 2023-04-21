// -*- coding: utf-8 -*-
//

// for the build system
#include <portinfo>
// support
#include <cassert>
// access to the CUDA memory allocators
#include <pyre/cuda/memory.h>
// and the journal
#include <pyre/journal.h>
// add the grid
#include <pyre/grid.h>
// get the timers
#include <pyre/timers.h>

// type alias
using canonical_t = pyre::grid::canonical_t<2>;
using pack_t = pyre::grid::canonical_t<2>;
using storage_t = pyre::cuda::memory::host_mapped_t<double>;
using grid_mapped_t = pyre::grid::grid_t<pack_t, storage_t>;
using proctimer_t = pyre::timers::process_timer_t;

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
    pack_t tensorPack { tensorShape };


    grid_mapped_t tensorArray { tensorPack, tensorPack.cells() };

    // create an array of arrays as pertubation of identity
    double pertubation = 0.1;
    int i, j, ij, jj;
    for (int nTensor = 0; nTensor < nTensors; nTensor++) {
        for (j = 0, ij = 0, jj = 0; j < 3; j++, jj += 4) {
            for (i = 0; i < 3; i++, ij++) {
                // Get the current index
                canonical_t::index_type index { ij, nTensor };
                // std::cout << "\nTesting index cpu: " << index << std::endl;
                // Compute the random perturbations
                tensorArray.at(index) = pertubation * (2 * (double) rand() / RAND_MAX - 1.0);
            }

            // Get the current index
            canonical_t::index_type index { jj, nTensor };
            tensorArray.at(index) += 1.0;
        }
    }

    // setup the grid for the gpu computation
    int nThreadPerBlock = 256;
    int nBlocks, nThreadLastBlock;

    // check if multiple blocks are necessary
    if (nTensors > nThreadPerBlock) {
        // allocate possibly too many workers
        nBlocks = nTensors / nThreadPerBlock + 1;

        // so check how many are in the last block
        nThreadLastBlock = nTensors - (nBlocks - 1) * nThreadPerBlock;

        // and remove the block if it is not used
        if (nThreadLastBlock == 0) {
            nBlocks -= 1;
            nThreadLastBlock = nThreadPerBlock;
        }
    } else {
        // if one block is enough
        nThreadPerBlock = nTensors;
        // allocate only one block
        nBlocks = 1;
        // easy
        nThreadLastBlock = nThreadPerBlock;
    }

    // determine the shape
    canonical_t::shape_type invariantShape { 1, nTensors };
    pack_t invariantPack { invariantShape };

    // allocate grids for return variables
    grid_mapped_t I1 { invariantPack, invariantPack.cells() };
    grid_mapped_t I2 { invariantPack, invariantPack.cells() };
    grid_mapped_t I3 { invariantPack, invariantPack.cells() };

    // make a timer
    proctimer_t timer("tests.timer");

    // and reset it
    timer.reset();

    // start the timer
    timer.start();

    // execute the kernel
    wrapInvariants(
        nBlocks, nThreadPerBlock, tensorArray.data()->device(), I1.data()->device(),
        I2.data()->device(), I3.data()->device(), nTensors);

    // wait for GPU to finish before stopping the timer
    auto status = cudaDeviceSynchronize();
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("pyre.cuda");
        // complain
        error << "while synchronizing the GPU " << pyre::journal::newline
              << cudaGetErrorName(status) << " (" << status << ")" << pyre::journal::endl(__HERE__);
        // and bail
        throw std::bad_alloc();
    }

    // and stop the timer
    timer.stop();

    // make a channel
    pyre::journal::debug_t timerChannel("tests.timer");
    // activate it
    timerChannel.activate();
    // show me
    timerChannel
        // show me the elapsed time
        << "elapsed time: " << timer.ms() << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}

// end of file
