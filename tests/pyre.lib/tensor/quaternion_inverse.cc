// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved
//


// support
#include <cassert>
// get the tensor algebra
#include <pyre/tensor.h>


// use namespace for readability
using namespace pyre::tensor;


// main program
int
main(int argc, char * argv[])
{
    // pick an angle
    auto angle = std::numbers::pi / 2.0;

    // pick an axis
    auto axis = normalize(vector_t<3> { 0.0, 0.0, 1.0 });

    // create a quaternion
    auto quaternion = quaternion_t(angle, axis);

    // pick a 3D vector
    auto a = vector_t<3> { 1.0, 0.0, 0.0 };

    // rotate {a} with the quaternion
    auto b = quaternion.rotation() * a;

    // create the quaternion representing the inverse rotation
    auto quaternion_inv = quaternion_t(-angle, axis);

    // rotate {b} with the inverse quaternion
    auto c = quaternion_inv.rotation() * b;

    // check that the composition of the two rotations is the identity
    assert(a == c);

    // all done
    return 0;
}


// end of file
