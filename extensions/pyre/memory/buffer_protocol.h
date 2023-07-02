// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_py_memory_buffer_protocol_h)
#define pyre_py_memory_buffer_protocol_h


// the {pyre} extension namespace
namespace pyre::py::memory {
    // add support for the python buffer protocol
    template <class memT>
    void bindBufferProtocol(shared_holder_t<memT> &);

} // namespace pyre::py::memory


// get the implementation
#define pyre_py_memory_buffer_protocol_icc
#include "buffer_protocol.icc"
#undef pyre_py_memory_buffer_protocol_icc

#endif

// end of file
