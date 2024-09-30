// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// external packages
#include "external.h"
// set up the namespace
#include "forward.h"

// published type aliases and declarations that constitute the public API of this package
// this is the file you are looking for
#include "api.h"

// base classes
#include "protocol/Node.h"
#include "protocol/Factory.h"
#include "protocol/Product.h"

// products
#include "products/Tile.h"
#include "products/Variable.h"

// factories
// arithmetic
#include "factories/Binary.h"
// addition
#include "factories/AddTiles.h"
#include "factories/AddVariables.h"
// multiplication
#include "factories/MultiplyTiles.h"
#include "factories/MultiplyVariables.h"

// end of file
