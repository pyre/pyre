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
// property lists
#include "PropList.h"
#include "DAPL.h"
#include "DCPL.h"
#include "DXPL.h"
#include "FAPL.h"
#include "FCPL.h"
#include "LAPL.h"
#include "LCPL.h"
// datatypes
#include "DataType.h"
#include "AtomType.h"
#include "PredType.h"
#include "IntType.h"
#include "FloatType.h"
#include "StrType.h"
#include "CompType.h"
#include "EnumType.h"
#include "ArrayType.h"
#include "VarLenType.h"

// implementation
#include "datatypes.h"
#include "datasets.h"


// end of file
