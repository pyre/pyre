// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(pyre_py_forward_h)
#define pyre_py_forward_h


// the {pyre} extension namespace
namespace pyre::py {
    // the module api
    void api(py::module &);

    // memory
    namespace memory {
        // the subpackage initializer
        void memory(py::module &);
        // file backed memory
        void map_c4(py::module &);
        void constmap_c4(py::module &);
        void map_c8(py::module &);
        void constmap_c8(py::module &);
    } // namespace memory

    // timers
    namespace timers {
        // the subpackage initializer
        void timers(py::module &);
        // timer types
        void wall_timers(py::module &);
        void process_timers(py::module &);
    } // namespace timers

} // namespace pyre::py


#endif

// end of file
