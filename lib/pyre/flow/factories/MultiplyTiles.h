// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// multiply two tiles to make a third
template <class op1T, class op2T, class resultT>
class pyre::flow::factories::Multiply<pyre::flow::products::tile_t, op1T, op2T, resultT> :
    public Binary<pyre::flow::products::tile_t, op1T, op2T, resultT> {
    // type aliases
public:
    // my base class
    using base_type = Binary<pyre::flow::products::tile_t, op1T, op2T, resultT>;
    // types from my superclass
    using name_type = typename base_type::name_type;
    using sentinel_type = typename base_type::sentinel_type;

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
    inline virtual auto make(const name_type & slot, typename base_type::product_ref_type product)
        -> typename base_type::factory_ref_type override;
};

// get the inline definitions
#include "MultiplyTiles.icc"

// end of file
