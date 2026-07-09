// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the bridge between python payloads and the buffers mpi moves
#include "utilities.h"


// add the bindings for the conduit
//
// what python adds to the conduit is the ability to move an arbitrary object, by flattening it
// into the raw payload the c++ layer already knows how to ship
void
pyre::mpi::py::port(py::module & m)
{
    // the class
    auto cls = py::class_<Port>(
        // in scope
        m,
        // the name
        "Port",
        // the docstring
        "a conduit between this process and one fixed peer");

    // the constructor, for anybody who would rather build one directly than ask a communicator
    cls.def(
        // the implementation
        py::init<Communicator, rank_t, tag_t>(),
        // the signature
        "communicator"_a, "peer"_a, "tag"_a = 0,
        // the docstring
        "build a conduit to {peer} over {communicator}, whose messages carry {tag}");

    // the structure
    cls.def_property_readonly(
        // the name
        "communicator",
        // the implementation
        &Port::communicator,
        // the docstring
        "the communicator my peer and i belong to");

    cls.def_property_readonly(
        // the name
        "peer",
        // the implementation
        &Port::peer,
        // the docstring
        "the process at the other end");

    cls.def_property_readonly(
        // the name
        "tag",
        // the implementation
        &Port::tag,
        // the docstring
        "the label my messages carry");

    // moving arbitrary objects; this, and only this, is what the bindings add to {pyre::mpi}
    cls.def(
        // the name
        "send",
        // the implementation
        [](const Port & self, const py::object & item) -> void {
            // flatten the object while we still hold the interpreter
            auto payload = pickle(item);
            // and ship it without holding it, so that other threads may run while mpi blocks
            py::gil_scoped_release nogil;
            // hand the octets to my peer
            self.sendBytes(payload);
            // all done
            return;
        },
        // the signature
        "item"_a,
        // the docstring
        "pack {item} and ship it to my peer");

    cls.def(
        // the name
        "recv",
        // the implementation
        [](const Port & self) -> py::object {
            // room for what arrives
            bytes_t payload;
            // take the message without holding the interpreter, since this blocks
            {
                py::gil_scoped_release nogil;
                payload = self.recvBytes();
            }
            // rebuild whatever my peer flattened
            return unpickle(payload);
        },
        // the docstring
        "block until my peer sends me something, and rebuild it");

    // moving text, which the c++ layer already knows how to do
    cls.def(
        // the name
        "sendString",
        // the implementation
        &Port::sendString,
        // block without holding the interpreter, so that other threads may run
        py::call_guard<py::gil_scoped_release>(),
        // the signature
        "message"_a,
        // the docstring
        "ship {message} to my peer, as text");

    cls.def(
        // the name
        "recvString",
        // the implementation
        &Port::recvString,
        // block without holding the interpreter, so that other threads may run
        py::call_guard<py::gil_scoped_release>(),
        // the docstring
        "block until my peer sends me text");

    // moving raw payloads
    cls.def(
        // the name
        "sendBytes",
        // the implementation
        [](const Port & self, const py::bytes & payload) -> void {
            // reinterpret the octets while we still hold the interpreter
            auto buffer = asBytes(payload);
            // and ship them without holding it
            py::gil_scoped_release nogil;
            // hand them to my peer
            self.sendBytes(buffer);
            // all done
            return;
        },
        // the signature
        "payload"_a,
        // the docstring
        "ship a raw payload to my peer");

    cls.def(
        // the name
        "recvBytes",
        // the implementation
        [](const Port & self) -> py::bytes {
            // room for what arrives
            bytes_t payload;
            // take the message without holding the interpreter, since this blocks
            {
                py::gil_scoped_release nogil;
                payload = self.recvBytes();
            }
            // and hand the octets to python
            return asPython(payload);
        },
        // the docstring
        "block until a raw payload arrives from my peer, and hand back exactly what came");

    // for the benefit of anybody staring at a prompt
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Port & self) -> string_t {
            return "<mpi.Port: peer " + std::to_string(self.peer()) + ", tag "
                 + std::to_string(self.tag()) + ">";
        },
        // the docstring
        "a human readable summary of this conduit");

    // all done
    return;
}


// end of file
