// -*- c++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2026 all rights reserved
//

#if !defined(pyre_extensions_mpi_external_h)
#define pyre_extensions_mpi_external_h

// pybind11
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// STL
#include <stdexcept>
#include <string>
#include <vector>

// pyre
#include <pyre/mpi.h>
#include <pyre/journal.h>

// convenience
namespace py = pybind11;
using namespace pybind11::literals;


// extension-local exception (pyre::mpi::Error already taken by the library)
namespace pyre::mpi::py {
    struct Error : std::runtime_error {
        using std::runtime_error::runtime_error;
    };
} // namespace pyre::mpi::py

#endif

// end of file
