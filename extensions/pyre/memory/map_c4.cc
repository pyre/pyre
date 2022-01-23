// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// wrappers over {pyre::memory::map} template expansions
// complex float
void
pyre::py::memory::map_c4(py::module & m)
{
    // alias
    using map_t = map_c4_t;

    // build the class record
    auto map = py::class_<map_t>(
        // the module scope
        m,
        // the name of the class
        "ComplexFloatMap",
        // its docstring
        "wrapper over a {pyre::memory::map_t<std::complex<float>>} buffer");

    // constructors
    map.def(
        // the constructor
        py::init<map_t::uri_type, bool>(),
        // the docstring
        "create a {c4} memory map over an existing file",
        // the signature
        "uri"_a, "writable"_a = false);

    map.def(
        // the constructor
        py::init<map_t::uri_type, map_t::size_type>(),
        // the docstring
        "create a new {c4} memory map with the given number of {cells}",
        // the signature
        "uri"_a, "cells"_a);

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

    map.def(
        // the name
        "__setitem__",
        // the implementation
        [](map_t & map, map_t::size_type index, map_t::value_type value) {
            // set the {value} at {index}
            map[index] = value;
            // all done
            return;
        },
        // the docstring
        "set the value of the element at a given index");

    // all done
    return;
}


// end of file
