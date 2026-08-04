// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// attribute creation property lists
void
pyre::h5::py::properties::acpl(py::module & m)
{
    // add bindings for hdf5 attribute creation property lists; everything they govern is
    // inherited from {strcpl}
    auto cls = py::class_<ACPL, STRCPL>(
        // in scope
        m,
        // class name
        "acpl",
        // docstring
        "an attribute creation property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) -> const ACPL & {
            // easy enough
            return ACPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default attribute creation property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build an attribute creation property list");

    // all done
    return;
}


// end of file
