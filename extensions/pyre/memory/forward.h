// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(pyre_py_memory_forward_h)
#define pyre_py_memory_forward_h


// the {pyre} extension namespace
namespace pyre::py::memory {
    // the initializer
    void memory(py::module &);
    // file backed memory
    void map_c4(py::module &);
    void constmap_c4(py::module &);
    void map_c8(py::module &);
    void constmap_c8(py::module &);
} // namespace pyre::py::memory


#endif

// end of file
