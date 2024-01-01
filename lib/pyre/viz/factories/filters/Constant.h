// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// generate a tile filled with a value
template <class constantT>
class pyre::viz::factories::filters::Constant : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my product
    using product_type = constantT;
    // my value type
    using cell_type = typename product_type::cell_type;

    // ref to me
    using factory_ref_type = std::shared_ptr<Constant>;
    // and to my products
    using product_ref_type = std::shared_ptr<product_type>;

    // factory
public:
    inline static auto create(const name_type & name = "", cell_type value = 0) -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Constant();
    // constructor; DON'T CALL
    inline Constant(sentinel_type, const name_type &, cell_type);

    // accessors
public:
    // get the tile fill value
    auto value() const -> cell_type;
    // get the product bound to my {tile} slot
    auto tile() -> product_ref_type;

    // mutators
public:
    // set the tile fill value
    auto value(cell_type value) -> factory_ref_type;
    // set the product bound to my {tile} slot
    auto tile(product_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(const name_type & slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // implementation details
private:
    cell_type _value;

    // suppressed metamethods
private:
    // constructors
    Constant(const Constant &) = delete;
    Constant & operator=(const Constant &) = delete;
    Constant(Constant &&) = delete;
    Constant & operator=(Constant &&) = delete;
};

// get the inline definitions
#include "Constant.icc"

// end of file
