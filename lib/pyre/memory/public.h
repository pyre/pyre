// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_memory_public_h)
#define pyre_memory_public_h


// external packages
#include "externals.h"
// get the forward declarations
#include "forward.h"

// published type aliases; this is the file you are looking for...
#include "api.h"

// implementation
#include "Cell.h"
// memory block on the stack
#include "Stack.h"
// memory block on the heap
#include "Heap.h"
// file-backed memory blocks
#include "FileMap.h"
#include "Map.h"
// foreign data
#include "View.h"


#endif

// end of file
