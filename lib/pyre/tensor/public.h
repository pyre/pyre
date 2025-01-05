// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved


// code guard
#if !defined(pyre_tensor_public_h)
#define pyre_tensor_public_h


// external packages
#include "externals.h"
// get the forward declarations
#include "forward.h"

// published type aliases; this is the file you are looking for...
#include "api.h"

// the repacking strategies
#include "repacking.h"
// get the concepts
#include "concepts.h"
// get the type traits
#include "traits.h"

// implementation
// functions to create tensors
#include "factories.h"
// the tensor
#include "Tensor.h"
// useful functions for {Tensor}
#include "utilities.h"
// {constexpr} version of {for} loops
#include "constexpr_for.h"
// the algebra on tensors
#include "algebra.h"
// the quaternions
#include "UnitQuaternion.h"


#endif

// end of file
