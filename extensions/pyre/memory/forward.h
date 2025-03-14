// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#if !defined(pyre_py_memory_forward_h)
#define pyre_py_memory_forward_h


// the {pyre} extension namespace
namespace pyre::py::memory {
    // bindings for buffers on the heap
    void heaps(py::module &);
    // bindings for file backed storage
    void maps(py::module &);
    // bindings for borrowed memory
    void views(py::module &);
} // namespace pyre::py::memory


#endif

// end of file
