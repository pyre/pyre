// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external packages
#include "external.h"
// set up the namespace
#include "forward.h"

// published type aliases and declarations that constitute the public API of this package
// this is the file you are looking for
#include "api.h"

// whether the mpi runtime is up; the handles and the errors both need to know
#include "state.h"
// the exception hierarchy, and the {check} that raises it
#include "Error.h"
// the shared ownership of an mpi handle
#include "traits.h"
#include "Handle.h"
// the vocabulary the message calls are phrased in
#include "datatypes.h"
#include "ops.h"
#include "threads.h"
// what mpi reports about a transfer, finished or not
#include "Status.h"
#include "Request.h"
// the structural entities
#include "Group.h"
#include "Communicator.h"
#include "Cartesian.h"
#include "Port.h"
// bringing mpi up and down, and the communicators it predefines
#include "runtime.h"


// end of file
