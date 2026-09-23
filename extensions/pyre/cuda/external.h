// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// get the extension support
#include "../external.h"
// the type-erased grid whose cells these bindings hand to cublas/cusolver/curand
#include <pyre/py/grid/AnyGrid.h>

// the cuda libraries; {WITH_CUDA} is what gates this whole subpackage, so these headers are
// only ever reached when the toolkit is actually there
#include <cuda_runtime_api.h>
#include <cublas_v2.h>
#include <cusolverDn.h>
#include <curand.h>


// end of file
