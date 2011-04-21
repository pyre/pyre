// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


// for the build system
#include <portinfo>

// grab the timer objects
#include <mpi.h>

// main program
int main() {
    // initialize
    MPI_Init(0, 0);
    // finalize
    MPI_Finalize();
    // all done
    return 0;
}

// end of file
