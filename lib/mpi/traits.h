// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the recipe for releasing a communicator
struct pyre::mpi::CommunicatorHandle {
    // types
public:
    // mpi hands out communicators as opaque handles; on some implementations these are
    // pointers, on others plain integers, so nothing here may assume either
    using handle_type = MPI_Comm;

    // interface
public:
    // hand {communicator} back to mpi; never throws, because this runs from a destructor
    static inline auto free(handle_type & communicator) noexcept -> void;
};


// the recipe for releasing a process group
struct pyre::mpi::GroupHandle {
    // types
public:
    // as above, an opaque handle
    using handle_type = MPI_Group;

    // interface
public:
    // hand {group} back to mpi; never throws, because this runs from a destructor
    static inline auto free(handle_type & group) noexcept -> void;
};


// get the inline definitions
#include "traits.icc"


// end of file
