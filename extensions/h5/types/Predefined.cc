// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// the package global declarations
#include "../__init__.h"
// the local declarations
#include "__init__.h"
// namespace setup
#include "forward.h"


// register the class of the predefined datatypes, so that every signature can name it; they have
// no interface beyond what they inherit
void
pyre::h5::py::types::predefinedClass(py::module & m)
{
    // register the class
    py::class_<PredType, AtomType>(
        // in scope
        m,
        // class name
        "predefined",
        // docstring
        "an HDF5 predefined datatype");

    // all done
    return;
}


// end of file
