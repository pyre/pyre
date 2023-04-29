// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2023 all rights reserved
//


// for the build system
#include <portinfo>

// access to the raw mpi routines
#include <pyre/mpi.h>
// and the journal
#include <pyre/journal.h>


// main program
int main(int argc, char *argv[]) {

    // initialize {mpi}
    MPI_Init(&argc, &argv);
    // initialize the journal
    pyre::journal::init(argc, argv);

    // build a handle to the world communicator
    pyre::mpi::communicator_t world(MPI_COMM_WORLD, true);
    // compute the size of the world group
    int wsize = world.size();
    // and my rank
    int wrank = world.rank();

    // make a channel
    pyre::journal::info_t channel("mpi.sanity");
    // but silence it
    channel.deactivate();

    // and say something
    channel
        << "[" << wrank << "/" << wsize << "]: hello world!"
        << pyre::journal::endl(__HERE__);

    // finalize mpi
    MPI_Finalize();

    // all done
    return 0;
}

// end of file
