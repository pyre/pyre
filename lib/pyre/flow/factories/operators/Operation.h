// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "../../externals.h"


// what the arithmetic needs to know about each operation: its name, the spelling of the alias
// that stands for it, and the combinations of tiles and scalars the math allows it; an operation
// that is not described here is not part of the arithmetic
namespace pyre::flow::factories::operators {
    // the general case is not implemented
    template <class operationT>
    struct Operation;
} // namespace pyre::flow::factories::operators


// addition, which the tiles are closed under; adding a scalar to a tile is shorthand for adding
// the tile whose every cell is that scalar
template <>
struct pyre::flow::factories::operators::Operation<std::plus<>> {
    // the name
    inline static auto name() -> string_t { return "add"; }
    // the human readable form of the name
    inline static auto className() -> string_t { return "Add"; }
    // the alias
    inline static auto decl() -> string_t { return "add_t"; }
    // two tiles
    static constexpr bool tiles = true;
    // a tile and a scalar
    static constexpr bool tileScalar = true;
    // a scalar and a tile
    static constexpr bool scalarTile = true;
};

// subtraction, which is addition of the opposite
template <>
struct pyre::flow::factories::operators::Operation<std::minus<>> {
    // the name
    inline static auto name() -> string_t { return "subtract"; }
    // the human readable form of the name
    inline static auto className() -> string_t { return "Subtract"; }
    // the alias
    inline static auto decl() -> string_t { return "subtract_t"; }
    // two tiles
    static constexpr bool tiles = true;
    // a tile and a scalar
    static constexpr bool tileScalar = true;
    // a scalar and a tile
    static constexpr bool scalarTile = true;
};

// multiplication, which scales a tile by a scalar on either side; the tiles are a vector space,
// so there is no product of two of them
template <>
struct pyre::flow::factories::operators::Operation<std::multiplies<>> {
    // the name
    inline static auto name() -> string_t { return "multiply"; }
    // the human readable form of the name
    inline static auto className() -> string_t { return "Multiply"; }
    // the alias
    inline static auto decl() -> string_t { return "multiply_t"; }
    // two tiles
    static constexpr bool tiles = false;
    // a tile and a scalar
    static constexpr bool tileScalar = true;
    // a scalar and a tile
    static constexpr bool scalarTile = true;
};

// division, which scales a tile by the inverse of a scalar; nothing divides by a tile
template <>
struct pyre::flow::factories::operators::Operation<std::divides<>> {
    // the name
    inline static auto name() -> string_t { return "divide"; }
    // the human readable form of the name
    inline static auto className() -> string_t { return "Divide"; }
    // the alias
    inline static auto decl() -> string_t { return "divide_t"; }
    // two tiles
    static constexpr bool tiles = false;
    // a tile and a scalar
    static constexpr bool tileScalar = true;
    // a scalar and a tile
    static constexpr bool scalarTile = false;
};


// end of file
