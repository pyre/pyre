// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// external packages
#include "externals.h"
// get the forward declarations
#include "forward.h"

// published type aliases; this is the file you are looking for...
#include "api.h"

// implementation
// thin wrapper over whatever a lightweight container
#include "Rep.h"
// packing order
#include "Order.h"
#include "OrderIterator.h"
// indices, shapes, and the canonical packing map
#include "Product.h"
#include "Shape.h"
#include "Index.h"
#include "IndexIterator.h"
#include "Canonical.h"
#ifdef HAVE_COMPACT_PACKINGS
#include "Symmetric.h"
#include "Diagonal.h"
#endif
// the grid
#include "Grid.h"
#include "GridIterator.h"

// the expansions
#include "expansions.h"


// end of file
