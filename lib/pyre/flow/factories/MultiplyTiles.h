// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
// my superclass
#include "Binary.h"

// multiply two tiles to make a third
template <class op1T, class op2T, class resultT>
class pyre::flow::factories::Multiply<pyre::flow::products::Tile, op1T, op2T, resultT> :
    public Binary<pyre::flow::products::Tile, op1T, op2T, resultT> {
    // type aliases
public:
    // me
    using self_type = Multiply<products::Tile, op1T, op2T, resultT>;
    // my superclass
    using super_type = Binary<products::Tile, op1T, op2T, resultT>;
    // types from my superclass
    using name_type = typename super_type::name_type;
    using sentinel_type = typename super_type::sentinel_type;

    // ref to me
    using factory_ref_type = std::shared_ptr<Multiply>;

    // factory
public:
    inline static auto create(const name_type & name = "") -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Multiply();
    // constructor; DON'T CALL
    inline Multiply(sentinel_type, const name_type &);

    // flow protocol
public:
    inline virtual auto make(const name_type & slot, typename super_type::product_ref_type product)
        -> typename super_type::factory_ref_type override;
};

// get the inline definitions
#include "MultiplyTiles.icc"

// end of file
