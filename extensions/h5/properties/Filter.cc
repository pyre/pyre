// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// one stage of the pipeline a dataset's cells pass through
void
pyre::h5::py::properties::filter(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<Filter>(
        // in scope
        m,
        // class name
        "Filter",
        // docstring
        "one stage of the pipeline a dataset's cells pass through");

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<H5Z_filter_t, string_t, unsigned int, unsigned int>(),
        // the signature
        "id"_a, "name"_a, "flags"_a, "configuration"_a,
        // the docstring
        "describe one stage of the pipeline a dataset's cells pass through");

    // which filter this is
    cls.def_readwrite(
        // the name
        "id",
        // the field
        &Filter::id,
        // the docstring
        "which filter this is");

    // what the library calls it
    cls.def_readwrite(
        // the name
        "name",
        // the field
        &Filter::name,
        // the docstring
        "what the library calls it");

    // how the library treats a failure of this stage
    cls.def_readwrite(
        // the name
        "flags",
        // the field
        &Filter::flags,
        // the docstring
        "how the library treats a failure of this stage");

    // whether the filter can encode, decode, or both
    cls.def_readwrite(
        // the name
        "configuration",
        // the field
        &Filter::configuration,
        // the docstring
        "whether the filter can encode, decode, or both");

    // all done
    return;
}


// end of file
