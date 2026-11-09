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
pyre::h5::py::properties::filterClass(py::module & m)
{
    // register the class of the record
    py::class_<Filter>(
        // in scope
        m,
        // class name
        "Filter",
        // docstring
        "one stage of the pipeline a dataset's cells pass through");

    // all done
    return;
}


// one stage of the pipeline a dataset's cells pass through
void
pyre::h5::py::properties::filter()
{
    // the class, registered by {filterClass}
    auto cls = py::class_<Filter>(py::type::of<Filter>());

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<H5Z_filter_t, string_t, unsigned int, unsigned int>(),
        // the signature
        "id"_a, "name"_a, "flags"_a, "configuration"_a,
        // the docstring
        "describe one stage of the pipeline a dataset's cells pass through");

    // which filter this is
    cls.def_property(
        // the name
        "id",
        // the getter
        pyre::py::getter(cls, &Filter::id),
        // the setter
        pyre::py::setter(cls, &Filter::id),
        // the docstring
        "which filter this is");

    // what the library calls it
    cls.def_property(
        // the name
        "name",
        // the getter
        pyre::py::getter(cls, &Filter::name),
        // the setter
        pyre::py::setter(cls, &Filter::name),
        // the docstring
        "what the library calls it");

    // how the library treats a failure of this stage
    cls.def_property(
        // the name
        "flags",
        // the getter
        pyre::py::getter(cls, &Filter::flags),
        // the setter
        pyre::py::setter(cls, &Filter::flags),
        // the docstring
        "how the library treats a failure of this stage");

    // whether the filter can encode, decode, or both
    cls.def_property(
        // the name
        "configuration",
        // the getter
        pyre::py::getter(cls, &Filter::configuration),
        // the setter
        pyre::py::setter(cls, &Filter::configuration),
        // the docstring
        "whether the filter can encode, decode, or both");

    // all done
    return;
}


// end of file
