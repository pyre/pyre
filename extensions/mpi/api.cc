// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add global bindings to the module
void
pyre::mpi::py::api(py::module & m)
{
    // bring mpi up
    m.def(
        // the name
        "initialize",
        // the implementation
        [](Thread required) -> Thread {
            // hand off to the runtime, which declines politely when mpi is already up
            return pyre::mpi::initialize(required);
        },
        // the signature
        "required"_a = Thread::single,
        // the docstring
        "bring mpi up, asking for the given level of thread support, and report what was granted");

    // take mpi down
    m.def(
        // the name
        "finalize",
        // the implementation
        []() -> void {
            // hand off to the runtime, which declines politely when mpi is down already
            pyre::mpi::finalize();
            // all done
            return;
        },
        // the docstring
        "take mpi down");

    // whether mpi is up
    m.def(
        // the name
        "initialized",
        // the implementation
        []() -> bool { return pyre::mpi::initialized(); },
        // the docstring
        "check whether mpi has been brought up");

    // whether mpi has been taken down
    m.def(
        // the name
        "finalized",
        // the implementation
        []() -> bool { return pyre::mpi::finalized(); },
        // the docstring
        "check whether mpi has been taken down");

    // the communicator that holds every process in the job
    m.def(
        // the name
        "world",
        // the implementation
        []() -> Communicator { return pyre::mpi::world(); },
        // the docstring
        "the communicator that holds every process in the job");

    // the communicator that holds this process alone
    m.def(
        // the name
        "self",
        // the implementation
        []() -> Communicator { return pyre::mpi::self(); },
        // the docstring
        "the communicator that holds this process alone");

    // the communicator that holds no processes at all
    m.def(
        // the name
        "null",
        // the implementation
        []() -> Communicator { return pyre::mpi::null(); },
        // the docstring
        "the communicator that holds no processes at all");

    // the clock
    m.def(
        // the name
        "wtime",
        // the implementation
        []() -> double { return pyre::mpi::wtime(); },
        // the docstring
        "seconds elapsed on this process since some fixed point in its past");

    // and its resolution
    m.def(
        // the name
        "wtick",
        // the implementation
        []() -> double { return pyre::mpi::wtick(); },
        // the docstring
        "the resolution of {wtime}, in seconds");

    // where this process lives
    m.def(
        // the name
        "processorName",
        // the implementation
        []() -> string_t { return pyre::mpi::processorName(); },
        // the docstring
        "the name of the host this process is running on");

    // the constants
    // the answer when mpi cannot place a process in a group
    m.attr("undefined") = pyre::mpi::undefined;
    // the wildcard that lets a receive match a message from any sender
    m.attr("anySource") = pyre::mpi::anySource;
    // the wildcard that lets a receive match a message carrying any label
    m.attr("anyTag") = pyre::mpi::anyTag;
    // the rank that names a peer with which communication is a no-op
    m.attr("procNull") = pyre::mpi::procNull;

    // all done
    return;
}


// end of file
