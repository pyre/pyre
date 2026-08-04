// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// dataset access property lists
void
pyre::h5::py::properties::dapl(py::module & m)
{
    // add bindings for hdf5 dataset access property lists
    auto cls = py::class_<DAPL, PropList>(
        // in scope
        m,
        // class name
        "dapl",
        // docstring
        "a dataset access property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) -> const DAPL & {
            // easy enough
            return DAPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default dataset access property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a dataset access property list");

    // interface
    // the chunk cache parameters
    cls.def_property(
        // the name
        "chunkCache",
        // the getter
        &DAPL::chunkCache,
        // the setter, which unpacks the {(slots, bytes, preemption policy)} triplet
        [](DAPL & self, const std::tuple<std::size_t, std::size_t, double> & cache) -> void {
            // spread the triplet
            auto [slots, bytes, w0] = cache;
            // and hand it to the property list
            self.setChunkCache(slots, bytes, w0);
            // all done
            return;
        },
        // the docstring
        "my chunk cache, as {(slots, bytes, preemption policy)}");


    // all done
    return;
}


// end of file
