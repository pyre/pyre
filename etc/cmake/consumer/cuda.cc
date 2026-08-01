// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the cuda layers; this header reaches both the cuda runtime and our own {pyre/memory.h}
// and {pyre/journal.h}, so it compiles only if the exported {pyre::cuda} target carries the
// cuda include directories and stands on {pyre}
#include <pyre/cuda.h>


// verify that the cuda add-on of an installation that carries it is reachable by a client that
// asks for the component and names nothing but {pyre::cuda}
// nothing here touches the driver api, so this passes on a machine with no gpu attached
int
main()
{
    // name a type from the wrappers; requiring it to be complete is what forces the compiler
    // to work through the cuda headers
    static_assert(sizeof(pyre::cuda::memory::managed_t<double>) > 0);

    // all done
    return 0;
}


// end of file
