// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the h5 wrappers; this header reaches {hdf5.h}, so it compiles only if the hdf5 include
// directories arrive through the exported {pyre::pyre} target, with no help from this project
#include <pyre/h5.h>
// and the version, so that we touch a symbol from {libpyre} as well
#include <pyre/version.h>


// verify that the hdf5 layer of an installation built against hdf5 is reachable by a client
// that names nothing but {pyre::pyre}
int
main()
{
    // name a type from the wrappers; requiring it to be complete is what forces the compiler
    // to work through {hdf5.h}
    static_assert(sizeof(pyre::h5::types::Datatype) > 0);

    // and pull something out of the library, so this is a link test as well as a compile test
    const auto version = pyre::version::version();
    // the major number of any real release is not negative
    if (std::get<0>(version) < 0) {
        // which makes this unreachable; it exists so the call cannot be optimized away
        return 1;
    }

    // all done
    return 0;
}


// end of file
