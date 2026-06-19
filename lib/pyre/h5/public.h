// -*- c++ -*-
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

// the pyre-owned wrappers over the hdf5 c api
#include "Identifier.h"
#include "DataSpace.h"
// property lists, in their own {properties} namespace
#include "properties/public.h"
// datatypes, in their own {types} namespace
#include "types/public.h"

// implementation
#include "datatypes.h"
#include "datasets.h"


// end of file
