// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external packages
#include "../external.h"
// set up the namespace
#include "forward.h"

// the pyre-owned hdf5 property lists
// the values a property list trades in
#include "ChunkCache.h"
#include "Alignment.h"
#include "Cache.h"
#include "PageBuffer.h"
#include "VersionBounds.h"
#include "FilespaceStrategy.h"
#include "Sizes.h"
#include "PhaseChange.h"
#include "LinkEstimate.h"
#include "Filter.h"
// the generic base
#include "List.h"
// the properties shared by everything one creates
#include "OCPL.h"
// the properties shared by everything that lays down a name
#include "STRCPL.h"
// dataset access, creation, and transfer
#include "DAPL.h"
#include "DCPL.h"
#include "DXPL.h"
// group creation
#include "GCPL.h"
// file access and creation
#include "FAPL.h"
#include "FCPL.h"
// link access and creation
#include "LAPL.h"
#include "LCPL.h"
// attribute creation
#include "ACPL.h"


// end of file
