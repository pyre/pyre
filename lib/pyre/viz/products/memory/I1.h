// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

class pyre::viz::products::memory::I1 : public pyre::flow::product_t {
    // type aliases
public:
    // my cell type
    using cell_type = pyre::viz::i1_t;
    // shared pointers to my  instances
    using ref_type = std::shared_ptr<I1>;

    // factory
public:
    inline static auto create(cell_type value = 0) -> ref_type;

    // metamethods
public:
    // destructor
    virtual ~I1();
    // constructor; DON'T CALL
    inline I1(sentinel_type, cell_type);

    // interface
public:
    // access to my data
    inline auto read() -> cell_type;
    inline auto write(cell_type value) -> ref_type;

    // implementation details - data
private:
    cell_type _value;

    // metamethods
private:
    // suppressed constructors
    I1(const I1 &) = delete;
    I1 & operator=(const I1 &) = delete;
    I1(I1 &&) = delete;
    I1 & operator=(I1 &&) = delete;
};


// get the inline definitions
#include "I1.icc"

// end of file
