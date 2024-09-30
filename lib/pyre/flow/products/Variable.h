// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

template <typename valueT>
class pyre::flow::products::Variable : public pyre::flow::product_t {
    // type aliases
public:
    // my cell type
    using cell_type = valueT;
    // shared pointers to my  instances
    using ref_type = std::shared_ptr<Variable>;

    // factory
public:
    inline static auto create(const name_type & name = "", cell_type value = 0) -> ref_type;

    // metamethods
public:
    // destructor
    virtual ~Variable();
    // constructor; DON'T CALL
    inline Variable(sentinel_type, const name_type &, cell_type);

    // my value as a control slot
public:
    inline auto value() -> cell_type;
    inline auto value(cell_type) -> ref_type;

    // interface
public:
    // value access by factories
    inline auto read() -> cell_type;
    inline auto write(cell_type value) -> ref_type;

    // implementation details - data
private:
    cell_type _value;

    // metamethods
private:
    // suppressed constructors
    Variable(const Variable &) = delete;
    Variable & operator=(const Variable &) = delete;
    Variable(Variable &&) = delete;
    Variable & operator=(Variable &&) = delete;
};


// get the inline definitions
#include "Variable.icc"

// end of file
