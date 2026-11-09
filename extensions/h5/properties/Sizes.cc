// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// register the class, so that every signature can name it
void
pyre::h5::py::properties::sizesClass(py::module & m)
{
    // register the class of the record
    py::class_<Sizes>(
        // in scope
        m,
        // class name
        "Sizes",
        // docstring
        "the widths hdf5 records positions and lengths in");

    // all done
    return;
}


// the widths hdf5 records positions and lengths in
void
pyre::h5::py::properties::sizes()
{
    // the class, registered by {sizesClass}
    auto cls = py::class_<Sizes>(py::type::of<Sizes>());

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<std::size_t, std::size_t>(),
        // the signature
        "offsets"_a, "lengths"_a,
        // the docstring
        "describe the widths hdf5 records positions and lengths in");

    // how many bytes a position in the file takes
    cls.def_property(
        // the name
        "offsets",
        // the getter
        pyre::py::getter(cls, &Sizes::offsets),
        // the setter
        pyre::py::setter(cls, &Sizes::offsets),
        // the docstring
        "how many bytes a position in the file takes");

    // how many bytes a length takes
    cls.def_property(
        // the name
        "lengths",
        // the getter
        pyre::py::getter(cls, &Sizes::lengths),
        // the setter
        pyre::py::setter(cls, &Sizes::lengths),
        // the docstring
        "how many bytes a length takes");

    // all done
    return;
}


// end of file
