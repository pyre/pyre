// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"

// my package declarations
#include "__init__.h"
// my subpackages
#include "properties/__init__.h"
#include "types/__init__.h"

// the module entry point
PYBIND11_MODULE(h5, m)
{
    // the docstring
    m.doc() = "the hdf5 extension module";

    // register the module api
    pyre::h5::py::api(m);
    // enums
    pyre::h5::py::enums(m);

    // subpackages
    pyre::h5::py::properties::__init__(m);
    pyre::h5::py::types::__init__(m);

    // object bindings
    pyre::h5::py::dataspace(m);
    pyre::h5::py::attribute(m);
    pyre::h5::py::dataset(m);
    pyre::h5::py::group(m);
    pyre::h5::py::file(m);

    // all done
    return;
}


// end of file
