// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_memory_Cell_h)
#define pyre_memory_Cell_h


// normalize access to a type
template <class T, bool isConst>
class pyre::memory::Cell {
    // types
public:
    // my cell
    using value_type = T;
    // derived types
    using pointer = std::conditional_t<isConst, const value_type *, value_type *>;
    using const_pointer = const value_type *;
    using reference = std::conditional_t<isConst, const value_type &, value_type &>;
    using const_reference = const value_type &;

    // distances
    using difference_type = ptrdiff_t;

    // sizes of things
    using size_type = size_t;
    // number of cells
    using cell_count_type = size_type;

    // interface
public:
    // compute the footprint of {n} cells
    static constexpr auto bytes(cell_count_type = 1) -> size_type;
};


// get the inline definitions
#define pyre_memory_Cell_icc
#include "Cell.icc"
#undef pyre_memory_Cell_icc


# endif

// end of file
