// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(h5_py_external_h)
#define h5_py_external_h


// STL
#include <string>
// support
#include <pyre/journal.h>
// pybind11
#include <pybind11/pybind11.h>
#include <pybind11/complex.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

// hdf5
#include <H5Cpp.h>


// type aliases
namespace h5::py {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals
    using namespace py::literals;

    // for decorating pybind11 classes
    // class names
    using classname_t = const char *;
    // docstrings
    using docstring_t = const char *;

    // wraper to install a {std::shared_ptr} as the custom holder for the bindings
    template <class classT>
    using shared_holder_t = py::class_<classT, std::shared_ptr<classT>>;

    // aliases for common STL classes
    using string_t = std::string;

    // aliases of hdf5 entities
    using File = H5::H5File;

} // namespace h5::py


#endif

// end of file
