// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_timers_forward_h)
#define pyre_py_timers_forward_h


// the {pyre} extension namespace
namespace pyre::py::timers {
    // the subpackage initializer
    void timers(py::module &);
    // timer types
    void wall_timers(py::module &);
    void process_timers(py::module &);
} // namespace pyre::py::timers


#endif

// end of file
