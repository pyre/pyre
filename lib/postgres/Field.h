// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// i share ownership of the result set my value lives in
#include "traits.h"
#include "Handle.h"
// i answer questions about the column my value came from
#include "status.h"
// and i turn its text into whatever the caller asked for
#include "codecs.h"
#include "Error.h"


// one value in a result set, together with what its column says it means
//
// a field is a view, not a value: the characters it hands out belong to the result set it came
// from. it keeps that set alive by holding a share of it, so a field may safely outlive the row
// and the result that produced it; the idiom {connection.exec(sql)[0][0].as<int>()} holds the
// result set alive through the field for the duration of the call
class pyre::postgres::Field {
    // types
public:
    // the shared owner of the result set i point into
    using storage_type = Handle<ResultHandle>;
    // row/column numbering
    using index_type = index_t;

    // metamethods
public:
    // point at the value in the given {row} and {column} of {result}
    inline Field(storage_type result, index_type row, index_type column);
    // the full set; copies share the result set, moves steal the share
    inline Field(const Field &) = default;
    inline Field(Field &&) noexcept = default;
    inline Field & operator=(const Field &) = default;
    inline Field & operator=(Field &&) noexcept = default;
    inline ~Field() = default;

    // where i am
public:
    // the row i came from
    inline auto row() const -> index_type;
    // the column i came from
    inline auto column() const -> index_type;
    // the name of that column, as the server labeled it
    inline auto name() const -> view_t;
    // the identifier of its type, as postgres catalogs it
    inline auto type() const -> oid_t;
    // whether its bytes are text or the internal representation of that type
    inline auto format() const -> Format;

    // what i hold
public:
    // whether the server sent nothing at all; a {NULL} is not the empty string, and the two
    // must never be confused: postgres draws a distinction here that c++ has no way to spell
    inline auto isNull() const -> bool;
    // the number of octets in my value; zero for a {NULL}, and zero for an empty string
    inline auto size() const -> index_type;
    // my value, exactly as it arrived, borrowed from the result set
    inline auto bytes() const -> view_t;

    // interface
public:
    // my value as a {valueT}; a {NULL} has no representation in most types, so asking for one
    // this way is an error, and the two calls below are how a caller says it might be absent
    template <typename valueT>
    inline auto as() const -> valueT;
    // my value as a {valueT}, or {fallback} when the server sent nothing
    template <typename valueT>
    inline auto as(valueT fallback) const -> valueT;
    // my value as a {valueT}, or nothing at all
    template <typename valueT>
    inline auto optional() const -> std::optional<valueT>;

    // contextual conversion to {bool}, true when i hold a value
    explicit inline operator bool() const;

    // implementation details
private:
    // the raw pointer to the result set, checked; a field of a result that somebody released
    // out from under it has nothing to point at
    inline auto _result() const -> ResultHandle::handle_type;

    // data
private:
    // the result set i point into, and my share of it
    storage_type _set;
    // where in it i am
    index_type _row;
    index_type _column;
};


// get the inline definitions
#include "Field.icc"


// end of file
