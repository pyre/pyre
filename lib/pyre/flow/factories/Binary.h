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
#include "../protocols/Factory.h"

// combine two operands to make a third
template <template <class> class categoryT, class op1T, class op2T, class resultT>
class pyre::flow::factories::Binary : public pyre::flow::protocols::Factory {
    // type aliases
public:
    // me
    using self_type = Binary<categoryT, op1T, op2T, resultT>;
    // my superclass
    using super_type = pyre::flow::protocols::Factory;
    // types from my superclass
    using name_type = typename super_type::name_type;
    using sentinel_type = typename super_type::sentinel_type;
    // my category
    template <class productT>
    using category_type = categoryT<productT>;
    // the products
    using op1_type = category_type<op1T>;
    using op2_type = category_type<op2T>;
    using result_type = category_type<resultT>;

    // ref to me
    using factory_ref_type = std::shared_ptr<super_type>;
    // and to my products
    using op1_ref_type = std::shared_ptr<op1_type>;
    using op2_ref_type = std::shared_ptr<op2_type>;
    using result_ref_type = std::shared_ptr<result_type>;

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
};

// get the inline definitions
#include "Binary.icc"

// end of file
