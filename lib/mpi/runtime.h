// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// the {check} that turns a failed mpi status into an exception
#include "Error.h"
// the two state queries, which live apart because everything below me needs them
#include "state.h"
// the levels of thread support i negotiate with
#include "threads.h"
// the communicators i hand back by value
#include "Communicator.h"


// bring mpi up, asking for the given level of thread support
auto
pyre::mpi::initialize(Thread required) -> Thread
{
    // room for the level mpi is willing to grant, which may be lower than the one we asked for
    int granted = MPI_THREAD_SINGLE;

    // a process that is already up cannot renegotiate its thread level
    if (initialized()) {
        // so just report what it settled on the first time
        check(MPI_Query_thread(&granted));
        // and hand it off
        return threadSupport(granted);
    }

    // otherwise, bring it up; there is no need to hunt down {argc} and {argv}, since the
    // launcher has already built the parallel machine by the time we get here
    check(MPI_Init_thread(nullptr, nullptr, threadLevel(required), &granted));

    // hand off the level we were granted
    return threadSupport(granted);
}


// take mpi down
auto
pyre::mpi::finalize() -> void
{
    // taking mpi down when it was never up, or twice, is an error
    if (!initialized() || finalized()) {
        // so decline
        return;
    }
    // otherwise, shut it down
    check(MPI_Finalize());
    // all done
    return;
}


// the communicator that holds every process in the job
auto
pyre::mpi::world() -> Communicator
{
    // mpi predefines it, so it is not ours to release
    return Communicator(MPI_COMM_WORLD, true);
}


// the communicator that holds this process alone
auto
pyre::mpi::self() -> Communicator
{
    // mpi predefines it, so it is not ours to release
    return Communicator(MPI_COMM_SELF, true);
}


// the communicator that holds no processes at all
auto
pyre::mpi::null() -> Communicator
{
    // mpi predefines it, so it is not ours to release
    return Communicator(MPI_COMM_NULL, true);
}


// seconds elapsed on this process since some fixed point in its past
auto
pyre::mpi::wtime() -> double
{
    // mpi reports no status for this one
    return MPI_Wtime();
}


// the resolution of {wtime}, in seconds
auto
pyre::mpi::wtick() -> double
{
    // nor for this one
    return MPI_Wtick();
}


// the name of the host this process is running on
auto
pyre::mpi::processorName() -> string_t
{
    // make room for the longest name mpi is allowed to produce
    char buffer[MPI_MAX_PROCESSOR_NAME];
    // and for its actual length
    int length = 0;
    // ask
    check(MPI_Get_processor_name(buffer, &length));
    // hand back exactly the characters mpi wrote
    return string_t(buffer, length);
}


// end of file
