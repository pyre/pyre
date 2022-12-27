// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_memory_forward_h)
#define pyre_py_memory_forward_h


// the {pyre} extension namespace
namespace pyre::py::memory {
    // the initializer
    void memory(py::module &);

    // bindings for file backed storage
    void maps(py::module &);

} // namespace pyre::py::memory


#endif

// end of file
