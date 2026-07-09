// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external dependencies, and the aliases that shape this namespace
#include "external.h"


// the bridge between python's payloads and the raw byte buffers {pyre::mpi} moves
namespace pyre::mpi::py {
    // reinterpret a python {bytes} object as a buffer mpi can ship
    auto asBytes(const py::bytes & payload) -> bytes_t;
    // and back
    auto asPython(const bytes_t & payload) -> py::bytes;

    // serialize an arbitrary python object into a buffer mpi can ship
    auto pickle(const py::object & item) -> bytes_t;
    // and reconstitute it
    auto unpickle(const bytes_t & payload) -> py::object;
} // namespace pyre::mpi::py


// end of file
