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
#include "Binary.h"

// combine two operands, each a scalar or a tile, with one of the operations of arithmetic
template <class operationT, class op1T, class op2T, class resultT>
    requires pyre::flow::factories::operators::arithmetic_c<operationT, op1T, op2T, resultT>
class pyre::flow::factories::operators::Arithmetic : public Binary<op1T, op2T, resultT> {
    // type aliases
public:
    // me
    using self_type = Arithmetic<operationT, op1T, op2T, resultT>;
    // my superclass
    using super_type = Binary<op1T, op2T, resultT>;
    // my operation
    using operation_type = operationT;
    // what i know about it
    using traits_type = Operation<operation_type>;
    // types from my superclass
    using name_type = typename super_type::name_type;
    using sentinel_type = typename super_type::sentinel_type;
    using product_ref_type = typename super_type::product_ref_type;
    // my products
    using op1_type = typename super_type::op1_type;
    using op2_type = typename super_type::op2_type;
    using result_type = typename super_type::result_type;

    // ref to me
    using factory_ref_type = std::shared_ptr<Arithmetic>;

    // the spelling of types
    using string_type = string_t;

    // the spelling of my type
public:
    // simulate my c++ declaration
    static inline auto declSelf() -> string_type;
    // the human readable form of my class name
    static inline auto className() -> string_type;

    // factory
public:
    inline static auto create(const name_type & name = "") -> factory_ref_type;

    // metamethods
public:
    // destructor
    inline virtual ~Arithmetic();
    // constructor; DON'T CALL
    inline Arithmetic(sentinel_type, const name_type &);

    // flow protocol
public:
    inline virtual auto make(const name_type & slot, product_ref_type product) ->
        typename super_type::factory_ref_type override;

    // implementation details
private:
    // check that the tiles among my operands have the shape of my result, and complain if not
    inline auto aligned() -> bool;

    // suppressed metamethods
private:
    // constructors
    Arithmetic(const Arithmetic &) = delete;
    Arithmetic & operator=(const Arithmetic &) = delete;
    Arithmetic(Arithmetic &&) = delete;
    Arithmetic & operator=(Arithmetic &&) = delete;
};

// get the inline definitions
#include "Arithmetic.icc"


// end of file
