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


// file objects
void
pyre::h5::py::types::__init__(py::module & m)
{
    // make a new namespace to hold datatype descriptions
    auto types = m.def_submodule(
        // the name of the module
        "types",
        // its docstring
        "HDF5 datatypes");

    // add the class definitions
    // the base data types
    datatype(types);
    // array datatypes
    array(types);
    // atom datatype
    atom(types);
    float_(types);
    int_(types);
    predefined(types);
    str(types);
    // compound datatypes
    compound(types);
    // enum types
    enum_(types);
    // variable length types
    varlen(types);

    // predefined datatypes
    native(types);

    std(types);
    big(types);
    little(types);

    alpha(types);
    ieee(types);
    intel(types);
    mips(types);
    unix(types);

    // all done
    return;
}


// end of file
