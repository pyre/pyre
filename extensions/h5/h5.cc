// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the module entry point
PYBIND11_MODULE(h5, m)
{
    // the docstring
    m.doc() = "the hdf5 extension module";

    // register the module api
    h5::py::api(m);

    // bindings
    h5::py::dataset(m);
    h5::py::datatypes::datatypes(m);
    h5::py::file(m);

    // all done
    return;
}


// end of file