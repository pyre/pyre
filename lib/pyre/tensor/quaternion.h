// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved
//


#if !defined(pyre_tensor_quaternion_h)
#define pyre_tensor_quaternion_h


namespace pyre::tensor {

    // composition of quaternions
    constexpr auto compose(const quaternion_t &, const quaternion_t &) -> quaternion_t;

} // namespace pyre::tensor


// get the inline definitions
#define pyre_tensor_quaternion_icc
#include "quaternion.icc"
#undef pyre_tensor_quaternion_icc


#endif

// end of file
