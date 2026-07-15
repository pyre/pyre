// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// i own the result set
#include "traits.h"
#include "Handle.h"
// i name the state the server left it in
#include "status.h"
// i hand back rows, by value
#include "Row.h"
// and i assemble the report that explains a failure
#include "Diagnostic.h"
#include "Error.h"


// everything the server sent back in answer to one statement
//
// a result owns its rows: it is the last thing standing between them and {PQclear}. copying one
// is a shared pointer copy, so results may be handed around freely, and the rows and fields
// taken out of them each keep them alive on their own
class pyre::postgres::Result {
    // types
public:
    // me
    using self_type = Result;
    // the opaque pointer libpq uses to name a result set
    using handle_type = PGresult *;
    // the shared owner of that pointer
    using storage_type = Handle<ResultHandle>;
    // what i hold
    using value_type = Row;
    // row/column numbering
    using index_type = index_t;

    // the walk down my rows, top to bottom
    class const_iterator;
    // there is no other kind; a result set arrives whole and never changes
    using iterator = const_iterator;

    // metamethods
public:
    // adopt the result set libpq just handed us
    explicit inline Result(handle_type result);
    // the full set; copies share the result set, moves steal it
    inline Result(const Result &) = default;
    inline Result(Result &&) noexcept = default;
    inline Result & operator=(const Result &) = default;
    inline Result & operator=(Result &&) noexcept = default;
    inline ~Result() = default;

    // structure
public:
    // the raw pointer, for handing to the libpq c api
    inline auto handle() const -> handle_type;
    // the state the server left the statement in
    inline auto status() const -> ExecStatus;
    // whether the statement ran
    inline auto ok() const -> bool;
    // contextual conversion to {bool}, true when the statement ran
    explicit inline operator bool() const;

    // shape
public:
    // how many rows the server sent
    inline auto rows() const -> index_type;
    // how many values each of them holds
    inline auto columns() const -> index_type;

    // the columns
public:
    // the label the server gave the given {column}
    inline auto name(index_type column) const -> view_t;
    // the position of the column the server labeled {name}, or {unknownColumn} when there is
    // no such column; this is the one query in the package that answers a question rather than
    // raising when it cannot
    inline auto column(view_t name) const -> index_type;
    // the identifier of the type of the given {column}, as postgres catalogs it
    inline auto type(index_type column) const -> oid_t;
    // whether the values in it are text or the internal representation of that type
    inline auto format(index_type column) const -> Format;

    // the values, reached directly; the rows and fields below are the pleasant way to do this,
    // and these are the way that allocates nothing at all
public:
    // whether the server sent nothing for the given {row} and {column}
    inline auto isNull(index_type row, index_type column) const -> bool;
    // the value there, borrowed
    inline auto value(index_type row, index_type column) const -> view_t;

    // the rows
public:
    // the given {row}
    inline auto operator[](index_type row) const -> value_type;
    // the same, spelled out
    inline auto row(index_type index) const -> value_type;

    // iteration
public:
    // my topmost row
    inline auto begin() const -> const_iterator;
    // one past my bottommost
    inline auto end() const -> const_iterator;

    // what the server said about the statement itself
public:
    // the tag the server put on it, e.g. {INSERT 0 1} or {SELECT 3}
    inline auto command() const -> view_t;
    // how many rows it touched; meaningful after an {insert}, {update} or {delete}, and zero
    // after everything else
    inline auto affected() const -> long;
    // the full report of what went wrong, blamed on {statement}
    inline auto diagnostic(string_t statement = "") const -> Diagnostic;
    // the one line rendering libpq assembled, borrowed
    inline auto message() const -> view_t;

    // interface
public:
    // classify this result and throw the matching exception; a caller that has just checked
    // {ok} and found it false uses this to turn the finding into a failure that carries the
    // server's own name for it
    [[noreturn]] inline auto raise(string_t statement = "") const -> void;

    // data
private:
    // the result set, and my share of it
    storage_type _set;
};


// the walk down the rows of a result set
class pyre::postgres::Result::const_iterator {
    // types
public:
    // what a standard algorithm needs to know about me
    using iterator_category = std::input_iterator_tag;
    using value_type = Row;
    using difference_type = std::ptrdiff_t;
    // a row is manufactured on demand rather than stored, so there is nothing to point at and
    // nothing to bind a reference to
    using pointer = void;
    using reference = Row;

    // metamethods
public:
    // stand at the given {row} of {result}
    inline const_iterator(storage_type result, index_type row);
    // the full set
    inline const_iterator(const const_iterator &) = default;
    inline const_iterator(const_iterator &&) noexcept = default;
    inline const_iterator & operator=(const const_iterator &) = default;
    inline const_iterator & operator=(const_iterator &&) noexcept = default;
    inline ~const_iterator() = default;

    // interface
public:
    // the row i stand at
    inline auto operator*() const -> reference;
    // move down one row
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
    index_type _row;
};


// get the inline definitions
#include "Result.icc"


// end of file
