// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// whether the mpi runtime is up, and whether it has been taken down
//
// these two live apart from the rest of {runtime.h} because almost everything below them needs
// to ask: a handle must know whether there is still an mpi to hand its token back to, and an
// error must know whether there is still an mpi to ask for a description. {runtime.h} itself
// cannot serve them, because it hands back communicators and so must sit above every entity in
// the package. the two questions here, by contrast, depend on nothing but {mpi.h}


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


// end of file
