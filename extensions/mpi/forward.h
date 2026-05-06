// -*- c++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2026 all rights reserved
//

#if !defined(pyre_extensions_mpi_forward_h)
#define pyre_extensions_mpi_forward_h

// forward declarations of the per-subsystem binding functions
namespace pyre::mpi::py {
    void communicator(::py::module &);
    void group(::py::module &);
    void ports(::py::module &);
    void startup(::py::module &);
} // namespace pyre::mpi::py

#endif

// end of file
