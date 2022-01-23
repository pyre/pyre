// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// the common storage binders
#include "bindings.h"
// my maps
#include "maps.h"


// wrappers over {pyre::memory::map} template expansions
// build the submodule
void
pyre::py::memory::maps(py::module & m)
{
    // const maps
    // c4
    constmap<std::complex<float>>(
        // in scope
        m,
        // class name
        "ComplexFloatConstMap",
        // docstring
        "a read-only file backed memory buffer of {std::complex<float>}");
    // c8
    constmap<std::complex<double>>(
        // in scope
        m,
        // class name
        "ComplexDoubleConstMap",
        // docstring
        "a read-only file backed memory buffer of {std::complex<double>}");

    // maps
    // c4
    map<std::complex<float>>(
        // in scope
        m,
        // class name
        "ComplexFloatMap",
        // docstring
        "a read/write file backed memory buffer of {std::complex<float>}");
    // c8
    map<std::complex<double>>(
        // in scope
        m,
        // class name
        "ComplexDoubleMap",
        // docstring
        "a read/write file backed memory buffer of {std::complex<double>}");

    // all done
    return;
}


// end of file
