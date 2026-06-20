// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// the package global declarations
#include "../__init__.h"
// the local declarations
#include "__init__.h"
// namespace setup
#include "forward.h"


// property lists
void
pyre::h5::py::properties::__init__(py::module & m)
{
    // make a new namespace to hold the property list classes
    auto properties = m.def_submodule(
        // the name of the module
        "properties",
        // its docstring
        "HDF5 property lists");

    // add the class definitions
    // the generic base
    pl(properties);
    // dataset access, creation, and transfer
    dapl(properties);
    dcpl(properties);
    dxpl(properties);
    // file access and creation
    fapl(properties);
    fcpl(properties);
    // link access and creation
    lapl(properties);
    lcpl(properties);

    // all done
    return;
}


// end of file
