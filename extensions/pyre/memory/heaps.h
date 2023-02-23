// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_memory_heaps_h)
#define pyre_py_memory_heaps_h


// the {pyre} extension namespace
namespace pyre::py::memory {
    // class record factory
    template <class cellT>
    void heap(py::module &, classname_t, docstring_t);
} // namespace pyre::py::memory


// get the implementation
#define pyre_py_memory_heaps_icc
#include "heaps.icc"
#undef pyre_py_memory_heaps_icc

#endif

// end of file
