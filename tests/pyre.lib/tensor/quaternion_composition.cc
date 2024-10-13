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
    auto angle_1 = std::numbers::pi / 2.0;

    // pick an axis
    auto axis_1 = normalize(vector_t<3> { 0.0, 0.0, 1.0 });

    // create a quaternion
    auto quaternion_1 = quaternion_t(angle_1, axis_1);

    // pick an angle
    auto angle_2 = std::numbers::pi / 2.0;

    // pick an axis
    auto axis_2 = normalize(vector_t<3> { 1.0, 0.0, 0.0 });

    // create a quaternion
    auto quaternion_2 = quaternion_t(angle_2, axis_2);

    // compose the two quaternions
    auto quaternion_3 = quaternion_2 * quaternion_1;

    // pick a 3D vector
    auto a = vector_t<3> { 1.0, 0.0, 0.0 };

    // rotate {a} with the quaternion
    auto b = quaternion_3.rotation() * a;

    // the expected result
    auto b_exact = vector_t<3> { 0.0, 0.0, 1.0 };

    // check that the expected result is obtained up to a reasonable tolerance
    assert(norm(b - b_exact) < 1.e-15);

    // all done
    return 0;
}


// end of file
