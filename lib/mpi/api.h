// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// externals
#include "external.h"
// forward declarations
#include "forward.h"


// the canonical names for the pyre-owned wrappers over the mpi c api
namespace pyre::mpi {
    // the exception hierarchy
    using error_t = Error;
    using mpiError_t = MPIError;
    using shapeError_t = ShapeError;

    // the outcome of a completed transfer, and the receipt of one still in flight
    using status_t = Status;
    using request_t = Request;

    // the structural entities
    using group_t = Group;
    using communicator_t = Communicator;
    using cartesian_t = Cartesian;

    // the reduction operators
    using op_t = Op;
} // namespace pyre::mpi


// end of file
