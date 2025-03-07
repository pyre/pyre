// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// externals
#include "externals.h"
// forward declarations
#include "forward.h"


// sentinel, used as a marker for the base of the cell type hierarchy
template <>
class pyre::memory::Cell<void, true> {};


// normalize access to a type
template <class T, bool isConst>
class pyre::memory::Cell : public Cell<void, true> {
    // types
public:
    // my type
    using self_type = Cell<T, isConst>;
    // my value
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
    // names
    using string_type = string_t;

    // interface
public:
    // expose my constness
    static constexpr auto readonly() -> bool;
    static constexpr auto writable() -> bool;
    // compute the footprint of {n} cells
    static constexpr auto bits(cell_count_type = 1) -> size_type;
    static constexpr auto bytes(cell_count_type = 1) -> size_type;

    // simulate my c++ declaration
    static inline auto declSelf() -> string_type;
    // simulate the c++ declaration of the template parameter
    static inline auto declValue() -> string_type;
    // generate a human readable name for my type
    static inline auto className() -> string_type;
};


// get the inline definitions
#include "Cell.icc"


// end of file
