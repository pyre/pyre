// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

// add two {i1_t}
class pyre::viz::factories::arithmetic::AddI1 : public pyre::flow::factory_t {
    // type aliases
public:
    // my base class
    using base_type = pyre::flow::factory_t;
    // my type
    using cell_type = pyre::viz::i1_t;
    // my product
    using product_type = products::memory::i1_t;
    // ref to me
    using factory_ref_type = std::shared_ptr<AddI1>;
    // and to my products
    using product_ref_type = std::shared_ptr<product_type>;


    // factory
public:
    inline static auto create() -> factory_ref_type;

    // metamethods
public:
    // destructor
    virtual ~AddI1();
    // constructor; DON'T CALL
    inline AddI1(sentinel_type);

    // accessors
public:
    inline auto op1() -> product_ref_type;
    inline auto op2() -> product_ref_type;
    inline auto result() -> product_ref_type;

    // mutators
public:
    auto op1(product_ref_type) -> factory_ref_type;
    auto op2(product_ref_type) -> factory_ref_type;
    auto result(product_ref_type) -> factory_ref_type;

    // flow protocol
public:
    virtual auto make(name_type slot, base_type::product_ref_type product)
        -> base_type::factory_ref_type override;

    // suppressed metamethods
private:
    // constructors
    AddI1(const AddI1 &) = delete;
    AddI1 & operator=(const AddI1 &) = delete;
    AddI1(AddI1 &&) = delete;
    AddI1 & operator=(AddI1 &&) = delete;
};

// get the inline definitions
#include "AddI1.icc"

// end of file