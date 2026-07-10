// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// i share ownership of the result set my values live in
#include "traits.h"
#include "Handle.h"
// i hand back fields, by value
#include "Field.h"
// and i complain when asked for a column that is not there
#include "Error.h"


// one row of a result set
//
// like a field, a row is a view that keeps its result set alive. it is cheap to copy, it may be
// iterated over, and its values may be reached either by position or by the name the server gave
// the column they came from
class pyre::postgres::Row {
    // types
public:
    // the shared owner of the result set i point into
    using storage_type = Handle<ResultHandle>;
    // what i hold
    using value_type = Field;

    // the walk across my fields, left to right
    class const_iterator;
    // there is no other kind; a result set arrives whole and never changes
    using iterator = const_iterator;

    // metamethods
public:
    // point at the given {row} of {result}
    inline Row(storage_type result, size_type row);
    // the full set; copies share the result set, moves steal the share
    inline Row(const Row &) = default;
    inline Row(Row &&) noexcept = default;
    inline Row & operator=(const Row &) = default;
    inline Row & operator=(Row &&) noexcept = default;
    inline ~Row() = default;

    // where i am
public:
    // my position in the result set
    inline auto index() const -> size_type;
    // how many values i hold, which is how many columns the result set has
    inline auto size() const -> size_type;

    // what i hold
public:
    // the value in the given {column}
    inline auto operator[](size_type column) const -> value_type;
    // the value in the column the server labeled {name}; postgres matches these the way it
    // matches an unquoted identifier, which is to say case insensitively
    inline auto operator[](view_t name) const -> value_type;

    // the same two, spelled out, for a caller who prefers the words
    inline auto field(size_type column) const -> value_type;
    inline auto field(view_t name) const -> value_type;

    // iteration
public:
    // my leftmost field
    inline auto begin() const -> const_iterator;
    // one past my rightmost
    inline auto end() const -> const_iterator;

    // implementation details
private:
    // the raw pointer to the result set, checked
    inline auto _result() const -> ResultHandle::handle_type;

    // data
private:
    // the result set i point into, and my share of it
    storage_type _set;
    // where in it i am
    size_type _row;
};


// the walk across the fields of a row
class pyre::postgres::Row::const_iterator {
    // types
public:
    // what a standard algorithm needs to know about me
    using iterator_category = std::input_iterator_tag;
    using value_type = Field;
    using difference_type = std::ptrdiff_t;
    // a field is manufactured on demand rather than stored, so there is nothing to point at
    // and nothing to bind a reference to
    using pointer = void;
    using reference = Field;

    // metamethods
public:
    // stand at the given {column} of the given {row} of {result}
    inline const_iterator(storage_type result, size_type row, size_type column);
    // the full set
    inline const_iterator(const const_iterator &) = default;
    inline const_iterator(const_iterator &&) noexcept = default;
    inline const_iterator & operator=(const const_iterator &) = default;
    inline const_iterator & operator=(const_iterator &&) noexcept = default;
    inline ~const_iterator() = default;

    // interface
public:
    // the field i stand at
    inline auto operator*() const -> reference;
    // move one column to the right
    inline auto operator++() -> const_iterator &;
    inline auto operator++(int) -> const_iterator;

    // whether two of us stand in the same place
    inline auto operator==(const const_iterator & other) const -> bool;
    inline auto operator!=(const const_iterator & other) const -> bool;

    // data
private:
    // the result set, and my share of it
    storage_type _set;
    // where i stand
    size_type _row;
    size_type _column;
};


// get the inline definitions
#include "Row.icc"


// end of file
