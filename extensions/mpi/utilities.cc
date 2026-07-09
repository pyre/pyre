// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// my declarations
#include "utilities.h"


// reinterpret a python {bytes} object as a buffer mpi can ship
auto
pyre::mpi::py::asBytes(const py::bytes & payload) -> bytes_t
{
    // pybind hands us the raw octets as a {std::string}, which is a container of {char}; it is
    // not text, and nobody downstream treats it as such
    auto octets = static_cast<std::string>(payload);
    // point at the first one
    auto first = reinterpret_cast<const std::byte *>(octets.data());
    // and copy the lot into a buffer whose cell type says what these really are
    return bytes_t(first, first + octets.size());
}


// turn a buffer mpi shipped back into a python {bytes} object
auto
pyre::mpi::py::asPython(const bytes_t & payload) -> py::bytes
{
    // point at the first octet
    auto first = reinterpret_cast<const char *>(payload.data());
    // and build the object from exactly as many as we hold; note the explicit length, without
    // which an embedded null would truncate the payload
    return py::bytes(first, payload.size());
}


// serialize an arbitrary python object into a buffer mpi can ship
auto
pyre::mpi::py::pickle(const py::object & item) -> bytes_t
{
    // reach for the serializer; the import is cheap after the first one, since python caches
    // every module it has already loaded
    auto pickle = py::module::import("pickle");
    // ask it to flatten {item}
    auto payload = pickle.attr("dumps")(item);
    // and hand back the octets
    return asBytes(payload.cast<py::bytes>());
}


// reconstitute an arbitrary python object from a buffer mpi shipped
auto
pyre::mpi::py::unpickle(const bytes_t & payload) -> py::object
{
    // reach for the serializer
    auto pickle = py::module::import("pickle");
    // and ask it to rebuild whatever the sender flattened
    return pickle.attr("loads")(asPython(payload));
}


// end of file
