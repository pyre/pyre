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


// encapsulations of the UNIX floating datatypes
void
pyre::h5::py::datatypes::unix(py::module & m)
{
    // make a new namespace to hold native datatype descriptions
    auto unix = m.def_submodule(
        // the name of the module
        "unix",
        // its docstring
        "the UNIX floating point types");

    // UNIX floating point
    unix.attr("d32be") = H5::PredType::UNIX_D32BE;
    unix.attr("d32le") = H5::PredType::UNIX_D32LE;
    unix.attr("d64be") = H5::PredType::UNIX_D64BE;
    unix.attr("d64le") = H5::PredType::UNIX_D64LE;

    // all done
    return;
}


// end of file
