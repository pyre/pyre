// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_h)
#define pyre_grid_h

// DESIGN NOTES

// Support for multi-dimensional arrays is an exercise in layering abstractions. At the lowest
// level, we must contend with basic memory representation constraints and its efficient
// access: machines are designed to present their memory as a linear expanse, and the hardware
// is optimized for fairly localized, if not entirely consecutive, access to a memory block. At
// the highest level, the programmer invents a multidimensional index space that presumably
// simplifies the realization of some algorithm. This package is an attempt to decompose this
// problem into irreducible parts and balance convenience with performance.

// In this package, we refer to a multidimensional array as a "grid". It's not a good name, but
// there are no good names for this problem. The best one i know of is "ndarray", and that's
// not very good at all. The work "grid" is supposed to remind you that this data structure is
// really a map from the user's abstract index space {I} to {Z_N} through an intermediate map
// that's the cartesian product of subsets of the non-negative integers

//  I: {I_0, I_1, ..., I_n-1} -> ... -> Z_{s_0} x Z_{s_2} x ... x Z_{s_{n-1}} -> Z_N -> memory

// where N = s_0 x s_1 x ... x s_n-1. The last step is provided by the language in terms of the
// built in {operator[]} and pointer arithmetic that map integer indices to typed memory. The
// second to the last forms the basis for supporting multi-dimensional arrays; it looks like
// mapping a cartesian grid to the integers, hence the name.

// The support in this package follows this chain of mappings from right to left. We start with
// a linear block of memory, add just enough structure to enable the multi-index abstraction,
// and cope with the complexities this generates. We then build the tools that enable
// generalized index spaces, handle some of the common cases, and leave the rest as an exercise
// for the student.

// Experience with the multitude of prior art in this space shows that a fundamental mistake is
// for an array to assume ownership and control of its memory block. In my opinion, this
// problem is entirely orthogonal to the index problem. In {pyre::memory}, there is a bunch of
// different ways to allocate and populate memory blocks, ranging from stealing someone else's,
// to dynamic allocation, to file-backed memory blocks that are the best way to handle truly
// large arrays with current operating systems. The solution in this package factors out this
// part of the problem, hence it works regardless of how the memory block is obtained.

// Given the address of the zeroth element of a memory block, C++ provides support for
// accessing the nth element of the block. The pointer to the block encodes the size of each
// cell in the block, and pointer arithmetic provides a map Z_n -> memory. Straightforward
// generalization of this requires:

// - an n-tuple {index_t} of integers that store the specific values of the index
// - an n-tuple {shape_t} that fixes the (s_1, m_2, ..., s_n)) in Z_s_1, ..., Z_s_N
// - a packing strategy, i.e. the actual map from the index space to Z_N

// The first two are relatively straightforward and describe the domain of the map. {shape_t}
// describes the domain of the map, and {index_t} is a point in this domain. We use
// {std::array} to represent both. The actual map is a bit more complicated. Ideally, it should
// be an isomorphism so that not only do indices map to a unique offset into the memory block,
// but the map is invertible to yield a unique index for each offset. There are many such maps
// (in fact, precisely N!). We are looking for the subset that has acceptable computational cost.

// The row major and column major packing strategies, familiar from 2-d arrays, can be
// generalized to arbitrary dimensions rather easily. Observe that in 2-d, with indices (i,j),
// both of these strategies map (0,0) to the beginning of the memory block, and pick an axis to
// vary first through its range of values while holding the other constant. When the fast index
// runs out of values, they bump the value of the other index by one, and run through the fast
// index values again. They represent essentially the same strategy with a different choice of
// fast index. In 2-d, there are only two choices for the fast index, so row major and column
// major is all there is. In n dimensions, one can capture all possible such maps by forming a
// permutation of the integers [0, n-1] and use it to determine the order in which the indices
// run.

// Other packing strategies are possible, many of which have very interesting properties. Space
// filling curves, such as the Morton Z curve or the Peano family of curves, are good examples
// of the trade offs between the computational complexity of the indexing map and the locality
// of the packing, i.e. the average distance in memory of cells that are nearest neighbors in
// index space.


// publish the interface
// the api is in "grid/api.h"
#include "grid/public.h"


#endif

// end of file
