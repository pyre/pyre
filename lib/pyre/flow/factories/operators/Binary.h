// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
// my superclass
#include "../../protocols/Factory.h"

// combine two operands to make a third
template <class op1T, class op2T, class resultT>
class pyre::flow::factories::operators::Binary : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = Binary<op1T, op2T, resultT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // types from my superclass
    using name_type = typename super_type::name_type;
    using sentinel_type = typename super_type::sentinel_type;
    // the products
    using op1_type = op1T;
    using op2_type = op2T;
    using result_type = resultT;

    // ref to me
    using factory_ref_type = std::shared_ptr<super_type>;
    // and to my products
    using op1_ref_type = std::shared_ptr<op1_type>;
    using op2_ref_type = std::shared_ptr<op2_type>;
    using result_ref_type = std::shared_ptr<result_type>;

    // the descriptions of my slots and settings
public:
    // the descriptions of my slots, shared by every factory of my type
    static inline auto declSlots() -> const slots_type &;
    // the descriptions of my settings, shared by every factory of my type
    static inline auto declSettings() -> const settings_type &;

    // introspection
public:
    // the descriptions of my slots
    inline virtual auto slots() const -> const slots_type & override;
    // the descriptions of my settings
    inline virtual auto settings() const -> const settings_type & override;

    // metamethods
public:
    // destructor
    inline virtual ~Binary() = default;
    // constructor; DON'T CALL
    inline Binary(sentinel_type, const name_type &);

    // accessors
public:
    auto op1() -> op1_ref_type;
    auto op2() -> op2_ref_type;
    auto result() -> result_ref_type;

    // mutators
public:
    auto op1(op1_ref_type op1) -> factory_ref_type;
    auto op2(op2_ref_type op2) -> factory_ref_type;
    auto result(result_ref_type result) -> factory_ref_type;

    // suppressed metamethods
private:
    // constructors
    Binary(const Binary &) = delete;
    Binary & operator=(const Binary &) = delete;
    Binary(Binary &&) = delete;
    Binary & operator=(Binary &&) = delete;
};

// get the inline definitions
#include "Binary.icc"


// end of file
