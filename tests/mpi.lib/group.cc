// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2023 all rights reserved
//


// for the build system
#include <portinfo>
//  other packages
#include <cassert>
// grab the mpi objects
#include <pyre/mpi.h>

typedef pyre::mpi::group_t group_t;
typedef pyre::mpi::communicator_t communicator_t;

// main program
int main() {
    // initialize
    MPI_Init(0, 0);

    // push down a scope to make sure our local variables get destroyed before MPI_Finalize
    {
        // build a handle to the world communicator
        communicator_t world(MPI_COMM_WORLD, true);
        // get its group
        group_t whole = world.group();

        // compute the size of the world group
        int size = whole.size();
        // and my rank
        int rank = whole.rank();

        // check: we know the makefile runs this test with 4 processes
        assert(size == 4);
        assert(rank >= 0 && rank < 4);
    }

    // shutdown
    MPI_Finalize();

    // all done
    return 0;
}

// end of file
