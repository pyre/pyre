// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// portability
#include <portinfo>
// support
#include <pyre/journal.h>
#include <pyre/flow.h>


// type aliases
// a packing
using packing_t = pyre::grid::canonical_t<2>;
// another one
using strided_t = pyre::grid::canonical_t<3>;
// tiles of reals
using real_t = pyre::flow::products::tile_t<
    pyre::grid::grid_t<packing_t, pyre::memory::heap_t<pyre::memory::float64_t>>>;
// of single precision reals
using single_t = pyre::flow::products::tile_t<
    pyre::grid::grid_t<packing_t, pyre::memory::heap_t<pyre::memory::float32_t>>>;
// of complex numbers
using complex_t = pyre::flow::products::tile_t<
    pyre::grid::grid_t<packing_t, pyre::memory::heap_t<pyre::memory::complex128_t>>>;
// of integers
using int_t = pyre::flow::products::tile_t<
    pyre::grid::grid_t<packing_t, pyre::memory::heap_t<pyre::memory::int32_t>>>;
// of reals laid out on a grid of another rank
using cube_t = pyre::flow::products::tile_t<
    pyre::grid::grid_t<strided_t, pyre::memory::heap_t<pyre::memory::float64_t>>>;
// scalars
using scalar_t = pyre::flow::products::var_t<pyre::memory::float64_t>;
using zscalar_t = pyre::flow::products::var_t<pyre::memory::complex128_t>;
using iscalar_t = pyre::flow::products::var_t<pyre::memory::int32_t>;

// the rule
template <class operationT, class op1T, class op2T, class resultT>
constexpr bool allowed =
    pyre::flow::factories::operators::arithmetic_c<operationT, op1T, op2T, resultT>;

// the operations
using add = std::plus<>;
using subtract = std::minus<>;
using multiply = std::multiplies<>;
using divide = std::divides<>;

// two scalars combine under every operation
static_assert(allowed<add, scalar_t, scalar_t, scalar_t>);
static_assert(allowed<subtract, scalar_t, scalar_t, scalar_t>);
static_assert(allowed<multiply, scalar_t, scalar_t, scalar_t>);
static_assert(allowed<divide, scalar_t, scalar_t, scalar_t>);

// tiles add and subtract
static_assert(allowed<add, real_t, real_t, real_t>);
static_assert(allowed<subtract, real_t, real_t, real_t>);
// but neither multiply nor divide each other, since they are a vector space
static_assert(!allowed<multiply, real_t, real_t, real_t>);
static_assert(!allowed<divide, real_t, real_t, real_t>);

// a scalar shifts a tile, on either side
static_assert(allowed<add, real_t, scalar_t, real_t>);
static_assert(allowed<add, scalar_t, real_t, real_t>);
static_assert(allowed<subtract, real_t, scalar_t, real_t>);
static_assert(allowed<subtract, scalar_t, real_t, real_t>);
// and scales it, on either side
static_assert(allowed<multiply, real_t, scalar_t, real_t>);
static_assert(allowed<multiply, scalar_t, real_t, real_t>);
// a tile divides by a scalar
static_assert(allowed<divide, real_t, scalar_t, real_t>);
// but nothing divides by a tile
static_assert(!allowed<divide, scalar_t, real_t, real_t>);

// the result of a tile and a scalar is a tile
static_assert(!allowed<multiply, real_t, scalar_t, scalar_t>);
// and the result of two scalars is a scalar
static_assert(!allowed<add, scalar_t, scalar_t, real_t>);

// complex numbers are numbers too
static_assert(allowed<add, complex_t, complex_t, complex_t>);
static_assert(allowed<multiply, zscalar_t, complex_t, complex_t>);
// and a real scalar scales a complex tile into a complex tile
static_assert(allowed<multiply, complex_t, scalar_t, complex_t>);
static_assert(allowed<divide, complex_t, scalar_t, complex_t>);
// but not into a real one, which would lose the imaginary parts
static_assert(!allowed<multiply, complex_t, scalar_t, real_t>);
// a complex scalar makes a complex tile of a real one
static_assert(allowed<multiply, real_t, zscalar_t, complex_t>);
// but not a real one
static_assert(!allowed<multiply, real_t, zscalar_t, real_t>);

// the result holds exactly the numbers the operation makes, so nothing is narrowed
static_assert(!allowed<add, real_t, real_t, single_t>);
// or widened behind the back of the user
static_assert(!allowed<add, single_t, single_t, real_t>);

// the integers do not divide, so they are left out of the arithmetic
static_assert(!allowed<add, int_t, int_t, int_t>);
static_assert(!allowed<divide, iscalar_t, iscalar_t, iscalar_t>);
static_assert(!allowed<multiply, real_t, iscalar_t, real_t>);

// tiles combine only with tiles that lay out their cells the same way
static_assert(!allowed<add, real_t, cube_t, real_t>);
static_assert(!allowed<multiply, cube_t, scalar_t, real_t>);

// an operation that is not part of the arithmetic is refused
static_assert(!allowed<std::modulus<>, scalar_t, scalar_t, scalar_t>);

// the aliases make a tile of a tile and a scalar, on either side
static_assert(std::same_as<
              pyre::flow::factories::operators::multiply_t<scalar_t, real_t>::result_type, real_t>);
static_assert(std::same_as<
              pyre::flow::factories::operators::multiply_t<real_t, scalar_t>::result_type, real_t>);
// and a scalar of two scalars
static_assert(
    std::same_as<pyre::flow::factories::operators::add_t<scalar_t>::result_type, scalar_t>);


// driver: the rules are checked by the compiler
int
main(int argc, char * argv[])
{
    // so there is nothing left to do
    return 0;
}


// end of file
