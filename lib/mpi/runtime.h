// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// bring mpi up, asking for the given level of thread support
auto
pyre::mpi::initialize(int required) -> int
{
    // room for the level mpi is willing to grant, which may be lower than the one we asked for
    int granted = MPI_THREAD_SINGLE;

    // bringing mpi up twice is an error, and harmless to attempt, since a process that is
    // already up cannot renegotiate its thread level
    if (initialized()) {
        // so just report what it settled on the first time
        check(MPI_Query_thread(&granted));
        // and hand it off
        return granted;
    }

    // otherwise, bring it up; there is no need to hunt down {argc} and {argv}, since the
    // launcher has already built the parallel machine by the time we get here
    check(MPI_Init_thread(nullptr, nullptr, required, &granted));

    // hand off the level we were granted
    return granted;
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


// whether {initialize} has been called
auto
pyre::mpi::initialized() -> bool
{
    // room for the answer
    int flag = 0;
    // this is one of the few calls that is legal before mpi comes up. deliberately do not run
    // the status through {check}: it would raise an {MPIError}, whose constructor asks this
    // very question in order to decide whether it may ask mpi to describe the failure, and the
    // two would recurse. a process whose runtime cannot answer this is not up, and saying so is
    // the only useful thing we can do
    MPI_Initialized(&flag);
    // hand it off
    return flag != 0;
}


// whether {finalize} has been called
auto
pyre::mpi::finalized() -> bool
{
    // room for the answer
    int flag = 0;
    // as above: legal at any point in the life of the process, and deliberately unchecked
    MPI_Finalized(&flag);
    // hand it off
    return flag != 0;
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
