// -*- c++ -*-
// -*- coding: utf-8 -*-
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


// encapsulations of the UNIX {time_t} representations
void
pyre::h5::py::types::unix(py::module & m)
{
    // make a new namespace to hold the {unix} specific representations
    auto unix = m.def_submodule(
        // the name of the module
        "unix",
        // its docstring
        "the standard unix {time_t} representations");

    // 32 and 64 bit times, in either byte order
    unix.attr("d32be") = PredType(H5T_UNIX_D32BE);
    unix.attr("d32le") = PredType(H5T_UNIX_D32LE);
    unix.attr("d64be") = PredType(H5T_UNIX_D64BE);
    unix.attr("d64le") = PredType(H5T_UNIX_D64LE);

    // all done
    return;
}


// end of file
