// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_memory_maps_h)
#define pyre_py_memory_maps_h


// the {pyre} extension namespace
namespace pyre::py::memory {
    // class record factories
    template <class cellT>
    void map(py::module &, classname_t, docstring_t);

    template <class cellT>
    void constmap(py::module &, classname_t, docstring_t);

} // namespace pyre::py::memory


// get the implementation
#define pyre_py_memory_maps_icc
#include "maps.icc"
#undef pyre_py_memory_maps_icc

#endif

// end of file
