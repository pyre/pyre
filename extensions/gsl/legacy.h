// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the method table is spelled in the vocabulary of the python c api
#include <Python.h>


// the entities that have not yet moved to pybind11
//
// these are still spelled as free functions over capsules, in the style of the python c api, and
// the module entry point grafts them onto the module it builds. the table shrinks with every
// class that gets bound, and both it and this header go away with the last of them
namespace gsl::legacy {
    // the method table the module publishes on their behalf
    extern PyMethodDef methods[];
} // namespace gsl::legacy


// end of file
