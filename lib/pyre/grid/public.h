// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_public_h)
#define pyre_grid_public_h


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
// the grid
#include "Grid.h"
#include "GridIterator.h"


#endif

// end of file
