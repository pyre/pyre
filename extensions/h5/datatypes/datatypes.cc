// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file objects
void
pyre::h5::py::datatypes::datatypes(py::module & m)
{
    // make a new namespace to hold datatype descriptions
    auto datatypes = m.def_submodule(
        // the name of the module
        "datatypes",
        // its docstring
        "HDF5 datatypes");

    // add the class definitions
    // the base data types
    datatype(datatypes);
    // compound datatypes
    compound(datatypes);
    // predefined datatypes
    predefined(datatypes);
    // add the constants that correspond to the native types
    native(datatypes);

    // all done
    return;
}


// end of file
