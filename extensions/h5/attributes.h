// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// code guard
#pragma once

// this decorator adds the shared attribute interface to each bound object; it lets the
// {pyre::h5::Location} interface be reused across groups, datasets, files, and named datatypes
// without binding {Location} itself

// extend the pyre::h5::py namespace
namespace pyre::h5::py {
    // decorator that adds access to the attributes of an h5 object
    template <class objectT>
    void attributes(py::class_<objectT> &);

} // namespace pyre::h5::py

// get the inline definitions
#include "attributes.icc"


// end of file
