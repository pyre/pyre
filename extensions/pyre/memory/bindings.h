// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_memory_bindings_h)
#define pyre_py_memory_bindings_h


// the {pyre} extension namespace
namespace pyre::py::memory {
    // decorate a storage class with bindings that do not require write access to {memT}
    template <class memT>
    void bindConstStorage(shared_holder_t<memT> &);

    // decorate a storage class with bindings that require write access to {memT}
    template <class memT>
    void bindStorage(shared_holder_t<memT> &);

} // namespace pyre::py::memory


// get the implementation
#define pyre_py_memory_bindings_icc
#include "bindings.icc"
#undef pyre_py_memory_bindings_icc

#endif

// end of file
