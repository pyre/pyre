// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// place everything in my private namespace
namespace pyre::extensions::cuda {

    // exceptions
    extern PyObject * Error;

    // exception registration
    extern const char * const registerExceptions__name__;
    extern const char * const registerExceptions__doc__;
    PyObject * registerExceptions(PyObject *, PyObject *);

} // namespace pyre::extensions::cuda


// end of file
