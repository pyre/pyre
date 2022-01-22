// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "../external.h"
// namespace setup
#include "../forward.h"


// wrappers over {pyre::memory::map} template expansions
// complex float
void
pyre::py::memory::constmap_c8(py::module & m)
{
    // alias
    using map_t = pyre::py::constmap_c8_t;

    // build the class record
    auto map = py::class_<map_t>(
        // the module scope
        m,
        // the name of the class
        "ConstComplexDouble",
        // its docstring
        "wrapper over a {pyre::memory::map_t<std::complex<double>>} buffer");

    // constructor
    map.def(
        // the constructor
        py::init<map_t::uri_type>(),
        // the docstring
        "create a read-only {c8} memory map over an existing file",
        // the signature
        "uri"_a);

    // cells
    map.def_property_readonly(
        // the name of the property
        "cells",
        // the getter
        &map_t::cells,
        // the docstring
        "the number of data cells");

    // bytes
    map.def_property_readonly(
        // the name of the property
        "bytes",
        // the getter
        &map_t::bytes,
        // the docstring
        "the memory footprint of the map, in bytes");

    // access
    map.def(
        // the name
        "__getitem__",
        // the implementtaion
        &map_t::at,
        // the docstring
        "get the value of the element at a given index");

    // all done
    return;
}


// end of file
