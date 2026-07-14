// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// place everything in my private namespace
namespace pyre::extensions::cuda {

    // setDevice
    const char * const setDevice__name__ = "setDevice";
    const char * const setDevice__doc__ = "allocate a device to the current thread";
    PyObject * setDevice(PyObject *, PyObject *);

    // resetDevice
    const char * const resetDevice__name__ = "resetDevice";
    const char * const resetDevice__doc__ = "reset the current device";
    PyObject * resetDevice(PyObject *, PyObject *);

} // namespace pyre::extensions::cuda


// end of file
