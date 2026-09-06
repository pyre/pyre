// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external packages
#include "externals.h"
// get the forward declarations
#include "forward.h"
// published type aliases; this is the file you are looking for...
#include "api.h"
// the template expansion machinery
#include "expansions.h"

// implementation
#include "Cell.h"
// scalars in a fixed byte order
#include "Ordered.h"
// bas class for memory buffers
#include "Buffer.h"
// memory block on the stack
#include "Stack.h"
// memory block on the heap
#include "Heap.h"
// file-backed memory blocks
#include "FileMap.h"
#include "Map.h"
// views on foreign data
#include "View.h"
// paged storage
#include "Paged.h"
// non-trivial iterator
#include "Slice.h"


// end of file
