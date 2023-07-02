// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file creation property lists
void
pyre::h5::py::fcpl(py::module & m)
{
    // add bindings for hdf5 file creation property lists
    auto cls = py::class_<FCPL, PropList>(
        // in scope
        m,
        // class name
        "FCPL",
        // docstring
        "a file creation property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) {
            // easy enough
            return &FCPL::DEFAULT;
        },
        // docstring
        "the default file creation property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a file creation property list");

    // interface
    // get the page size
    cls.def(
        // the name
        "getPageSize",
        // the implementation
        &FCPL::getFileSpacePagesize,
        // the signature
        // the docstring
        "retrieve the file space page size");

    // set the page size
    cls.def(
        // the name
        "setPageSize",
        // the implementation
        &FCPL::setFileSpacePagesize,
        // the signature
        "size"_a,
        // the docstring
        "set the file space page {size}");

    // get the file space strategy
    cls.def(
        // the name
        "getFilespaceStrategy",
        // the implementation
        [](FCPL & self) {
            // make some room
            H5F_fspace_strategy_t strategy;
            hbool_t persist;
            hsize_t threshold;
            // read the strategy
            self.getFileSpaceStrategy(strategy, persist, threshold);
            // pack them and return them
            return py::make_tuple(strategy, persist, threshold);
        },
        // the docstring
        "get the current file space strategy");

    // set the file space strategy
    cls.def(
        // the name
        "setFilespaceStrategy",
        // the implementation
        [](FCPL & self, H5F_fspace_strategy_t strategy, hbool_t persist, hsize_t threshold) {
            // set the strategy
            self.setFileSpaceStrategy(strategy, persist, threshold);
            // all done
            return;
        },
        // the signature
        "strategy"_a, "persist"_a, "threshold"_a,
        // the docstring
        "set the file space strategy");

    // all done
    return;
}


// end of file
