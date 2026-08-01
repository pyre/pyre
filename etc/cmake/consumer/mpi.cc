// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the mpi wrappers; this header reaches {mpi.h}, so it compiles only if the mpi usage
// requirements arrive through the exported {pyre::mpi} target
#include <pyre/mpi.h>


// verify that the mpi add-on of an installation that carries it is reachable by a client that
// asks for the component and names nothing but {pyre::mpi}
// there is no {MPI_Init} here on purpose: this checks the package, not the runtime, so it has
// to pass outside {mpiexec}
int
main()
{
    // name a type from the wrappers; requiring it to be complete is what forces the compiler
    // to work through {mpi.h}
    static_assert(sizeof(pyre::mpi::communicator_t) > 0);

    // all done
    return 0;
}


// end of file
