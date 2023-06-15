// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"

// my package declarations
#include "__init__.h"
// my subpackages
#include "datatypes/__init__.h"

// the module entry point
PYBIND11_MODULE(h5, m)
{
    // the docstring
    m.doc() = "the hdf5 extension module";

    // register the module api
    pyre::h5::py::api(m);
    // enums
    pyre::h5::py::enums(m);
    // property lists
    pyre::h5::py::pl(m);
    pyre::h5::py::dapl(m);
    pyre::h5::py::dcpl(m);
    pyre::h5::py::dxpl(m);
    pyre::h5::py::fapl(m);
    pyre::h5::py::fcpl(m);
    pyre::h5::py::lapl(m);
    pyre::h5::py::lcpl(m);

    // subpackages
    pyre::h5::py::datatypes::__init__(m);

    // object bindings
    pyre::h5::py::dataspace(m);
    pyre::h5::py::dataset(m);
    pyre::h5::py::group(m);
    pyre::h5::py::file(m);

    // all done
    return;
}


// end of file
