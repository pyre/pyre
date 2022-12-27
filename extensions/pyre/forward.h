// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_forward_h)
#define pyre_py_forward_h


// the {pyre} extension namespace
namespace pyre::py {
    // the module api
    void api(py::module &);

    // grid
    namespace grid {
        // the initializer
        void grid(py::module &);
    } // namespace grid

    // memory
    namespace memory {
        // the initializer
        void memory(py::module &);
    } // namespace memory

    // timers
    namespace timers {
        // the subpackage initializer
        void timers(py::module &);
    } // namespace timers

    // viz
    namespace viz {
        // the subpackage initializer
        void viz(py::module &);
    } // namespace viz

} // namespace pyre::py


#endif

// end of file
