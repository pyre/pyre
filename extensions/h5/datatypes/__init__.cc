// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// the package globla declarations
#include "../__init__.h"
// the local declarations
#include "__init__.h"
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
    // array datatypes
    array(datatypes);
    // atom datatype
    atom(datatypes);
    float_(datatypes);
    int_(datatypes);
    predefined(datatypes);
    str(datatypes);
    // compound datatypes
    compound(datatypes);
    // add the constants that correspond to the native types
    native(datatypes);
    // enum types
    enum_(datatypes);
    // variable length types
    varlen(datatypes);

    // all done
    return;
}


// end of file