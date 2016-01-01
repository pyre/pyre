// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// externals
#include <portinfo>
#include <Python.h>
#include <pyre/timers.h>

// access the declarations
#include "display.h"

namespace pyre {
    namespace extensions {
        namespace timers {

            // the capsule tag
            const char * const timerCapsuleName = "pyre.timers.timer";
        } // of namespace timers
    } // of namespace extensions
} // of namespace pyre


// newTimer
PyObject * pyre::extensions::timers::newTimer(PyObject *, PyObject * args)
{
    // the name of the timer
    const char * name;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "s:newTimer", &name)) {
        return 0;
    }
    // access the timer
    pyre::timer_t::timer_t * timer = & pyre::timer_t::retrieveTimer(name);
    // encapsulate it
    PyObject * capsule = PyCapsule_New(timer, timerCapsuleName, 0);
    // and return the capsule
    return capsule;
}

// start
PyObject * pyre::extensions::timers::start(PyObject *, PyObject * args)
{
    // the capsule with the timer pointer
    PyObject * capsule;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!:start", &PyCapsule_Type, &capsule)) {
        return 0;
    }
    // bail if the capsule is invalid
    if (!PyCapsule_IsValid(capsule, timerCapsuleName)) {
        return 0;
    }
    // cast it to a Timer pointer
    pyre::timer_t::timer_t * timer
        = static_cast<pyre::timer_t::timer_t *>(PyCapsule_GetPointer(capsule, timerCapsuleName));
    // start the timer
    timer->start();
    // and return None
    Py_INCREF(Py_None);
    return Py_None;
}

// stop
PyObject * pyre::extensions::timers::stop(PyObject *, PyObject * args)
{
    // the capsule with the timer pointer
    PyObject * capsule;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!:start", &PyCapsule_Type, &capsule)) {
        return 0;
    }
    // bail if the capsule is invalid
    if (!PyCapsule_IsValid(capsule, timerCapsuleName)) {
        return 0;
    }
    // cast it to a Timer pointer
    pyre::timer_t::timer_t * timer
        = static_cast<pyre::timer_t::timer_t *>(PyCapsule_GetPointer(capsule, timerCapsuleName));
    // start the timer
    timer->stop();
    // and return None
    Py_INCREF(Py_None);
    return Py_None;
}

// reset
PyObject * pyre::extensions::timers::reset(PyObject *, PyObject * args)
{
    // the capsule with the timer pointer
    PyObject * capsule;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!:start", &PyCapsule_Type, &capsule)) {
        return 0;
    }
    // bail if the capsule is invalid
    if (!PyCapsule_IsValid(capsule, timerCapsuleName)) {
        return 0;
    }
    // cast it to a Timer pointer
    pyre::timer_t::timer_t * timer
        = static_cast<pyre::timer_t::timer_t *>(PyCapsule_GetPointer(capsule, timerCapsuleName));
    // stop the timer
    timer->reset();
    // and return None
    Py_INCREF(Py_None);
    return Py_None;
}

// read
PyObject * pyre::extensions::timers::read(PyObject *, PyObject * args)
{
    // the capsule with the timer pointer
    PyObject * capsule;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!:start", &PyCapsule_Type, &capsule)) {
        return 0;
    }
    // bail if the capsule is invalid
    if (!PyCapsule_IsValid(capsule, timerCapsuleName)) {
        return 0;
    }
    // cast it to a Timer pointer
    pyre::timer_t::timer_t * timer
        = static_cast<pyre::timer_t::timer_t *>(PyCapsule_GetPointer(capsule, timerCapsuleName));
    // start the timer
    double elapsed = timer->read();
    // and return the time elapsed
    return Py_BuildValue("d", elapsed);
}

// lap
PyObject * pyre::extensions::timers::lap(PyObject *, PyObject * args)
{
    // the capsule with the timer pointer
    PyObject * capsule;
    // extract the arguments
    if (!PyArg_ParseTuple(args, "O!:start", &PyCapsule_Type, &capsule)) {
        return 0;
    }
    // bail if the capsule is invalid
    if (!PyCapsule_IsValid(capsule, timerCapsuleName)) {
        return 0;
    }
    // cast it to a Timer pointer
    pyre::timer_t::timer_t * timer
        = static_cast<pyre::timer_t::timer_t *>(PyCapsule_GetPointer(capsule, timerCapsuleName));
    // reset the timer
    double elapsed = timer->lap();
    // and return the time elapsed
    return Py_BuildValue("d", elapsed);
}

// end of file
