// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// translate one of my levels into the constant mpi expects
auto
pyre::mpi::threadLevel(Thread thread) -> int
{
    // dispatch on the level
    switch (thread) {
        // only one thread will execute
        case Thread::single:
            return MPI_THREAD_SINGLE;
        // only the thread that brought mpi up will call it
        case Thread::funneled:
            return MPI_THREAD_FUNNELED;
        // any thread may call mpi, but never two at once
        case Thread::serialized:
            return MPI_THREAD_SERIALIZED;
        // any thread may call mpi at any time
        case Thread::multiple:
            return MPI_THREAD_MULTIPLE;
    }

    // a level outside the enumeration means somebody added a case and forgot this switch
    auto channel = pyre::journal::firewall_t("pyre.mpi.thread");
    // complain
    channel
        // what
        << "unknown level of thread support"
        << pyre::journal::newline
        // details
        << "value: " << static_cast<int>(thread)
        // where, and flush
        << pyre::journal::endl(__HERE__);

    // not reached, since the firewall is fatal; here so every path returns
    return MPI_THREAD_SINGLE;
}


// translate mpi's answer back into one of my labels
auto
pyre::mpi::threadSupport(int level) -> Thread
{
    // only one thread will execute
    if (level == MPI_THREAD_SINGLE) {
        return Thread::single;
    }
    // only the thread that brought mpi up will call it
    if (level == MPI_THREAD_FUNNELED) {
        return Thread::funneled;
    }
    // any thread may call mpi, but never two at once
    if (level == MPI_THREAD_SERIALIZED) {
        return Thread::serialized;
    }
    // any thread may call mpi at any time
    if (level == MPI_THREAD_MULTIPLE) {
        return Thread::multiple;
    }

    // anything else means mpi granted a level its own standard does not define
    auto channel = pyre::journal::firewall_t("pyre.mpi.thread");
    // complain
    channel
        // what
        << "unknown level of thread support"
        << pyre::journal::newline
        // details
        << "value: " << level
        // where, and flush
        << pyre::journal::endl(__HERE__);

    // not reached, since the firewall is fatal; here so every path returns
    return Thread::single;
}


// end of file
