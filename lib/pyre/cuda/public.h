// -*- C++ -*-
// -*- coding: utf-8 -*-
//

// code guard
#if !defined(pyre_cuda_public_h)
#define pyre_cuda_public_h

// forward declaration
#include "forward.h"

// the object model
#include "ComputeCapability.h"
#include "Device.h"

// the implementations
#define pyre_cuda_ComputeCapability_icc
#include "ComputeCapability.icc"
#undef pyre_cuda_ComputeCapability_icc

#define pyre_cuda_Device_icc
#include "Device.icc"
#undef pyre_cuda_Device_icc

#endif

// end of file
