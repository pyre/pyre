// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// place everything in my private namespace
namespace pyre::extensions::cuda {

    // discover
    const char * const discover__name__ = "discover";
    const char * const discover__doc__ = "device discovery";
    PyObject * discover(PyObject *, PyObject *);

} // namespace pyre::extensions::cuda


// end of file
