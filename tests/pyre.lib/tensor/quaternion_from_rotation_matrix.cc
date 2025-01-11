// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved
//


// support
#include <cassert>
#include <numbers>
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

    // get the rotation matrix associated with this quaternion
    auto R = quaternion.rotation();

    // create another quaternion representing this rotation
    auto quaternion_prime = quaternion_t(R);

    // get the angle of rotation for this new quaternion
    auto angle_prime = quaternion_prime.angle();

    // get the axis of rotation for this new quaternion
    auto axis_prime = quaternion_prime.axis();

    // check that the two quaternions are equivalent up to a reasonable tolerance
    assert(std::fabs(angle - angle_prime) < 1.e-15);
    assert(axis == axis_prime);

    // all done
    return 0;
}


// end of file
