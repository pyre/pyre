// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved
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
    // pick a unit vector
    auto v1 = vector_t<3> { 1.0, 1.0, 1.0 };
    v1 = normalize(v1);

    // pick another unit vector
    auto v2 = vector_t<3> { 2.0, -1.0, 1.0 };
    v2 = normalize(v2);

    // assemble the rotation matrix that takes v1 to v2 using the Rodrigues formula
    auto a = cross(v1, v2);
    auto c = dot(v1, v2);
    auto lambda = identity<matrix_t<3>> + skew(a) + skew(a) * skew(a) * (1.0 / (1.0 + c));

    // apply the rotation to v1
    auto v2_prime = lambda * v1;

    // check that the result is correct
    assert(norm(v2_prime - v2) < 1.e-15);

    // all done
    return 0;
}


// end of file
