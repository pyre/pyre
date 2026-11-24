// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// i hold a share of the session i run on, and its lock
#include "Connection.h"


// a copy of rows into a table, from a {COPY … FROM STDIN}
//
// the rows travel as lines of the text format of a copy: the values of a row are separated by
// tabs, a {NULL} is spelled {\N}, and the tab, the newline, the carriage return and the backslash
// inside a value are escaped with a backslash. each value is the text its type reads, which is
// the text the codecs make for the placeholders of a statement
//
// a copy holds the lock of its session from the moment it starts until it ends, so that no other
// thread can send a statement that would abandon it; it is used by the thread that started it.
// it ends when {end} keeps its rows or {abort} throws them away, and a copy that goes away
// before either throws them away
//
// a copy may not be copied, because what it started on the server can be ended only once; it
// may be moved, because the obligation to end it can be handed on
class pyre::postgres::CopyIn {
    // types
public:
    // me
    using self_type = CopyIn;
    // the session
    using connection_type = Connection;
    // the hold on its lock
    using guard_type = Connection::guard_type;
    // the values of a row, as the text their types read
    using arguments_type = arguments_t;

    // metamethods
public:
    // start the copy {statement}, a {COPY … FROM STDIN}, on {connection}
    explicit inline CopyIn(connection_type connection, view_t statement);
    // what i started on the server can be ended only once, so there is exactly one of me
    CopyIn(const CopyIn &) = delete;
    CopyIn & operator=(const CopyIn &) = delete;
    // but the duty to end it may be passed along
    inline CopyIn(CopyIn && other) noexcept;
    inline CopyIn & operator=(CopyIn && other) noexcept;
    // and whoever ends up holding it throws its rows away, unless they were kept
    inline ~CopyIn();

    // interface
public:
    // send {data}, any number of whole rows in the text format of a copy
    inline auto put(view_t data) -> void;
    // send one row, whose values are the text their types read; a missing value is {NULL}
    inline auto row(const arguments_type & values) -> void;
    // the same, with the values given as themselves rather than as text
    template <typename... argsT>
    inline auto record(const argsT &... values) -> void;
    // keep the rows, and hand back what the server said, which counts them
    inline auto end() -> Result;
    // throw the rows away, giving the server {reason}
    inline auto abort(view_t reason) -> void;
    // whether neither {end} nor {abort} has been called
    inline auto live() const -> bool;
    // the statement that started me
    inline auto statement() const -> view_t;

    // implementation details
private:
    // make sure the copy is still under way
    inline auto _check() const -> void;
    // add {value}, escaped, to the {line} of a row
    static inline auto _escape(string_t & line, view_t value) -> void;
    // the copy is over: collect the answer of the server, let go of the session, and raise
    // when the server refused the rows
    inline auto _finish() -> Result;
    // throw the rows away and swallow whatever goes wrong; the destructor calls this
    inline auto _close() noexcept -> void;

    // data
private:
    // the session, and my share of it
    connection_type _connection;
    // the hold on its lock
    guard_type _guard;
    // the statement that started me
    string_t _statement;
    // whether the copy is under way
    bool _live;
};


// get the inline definitions
#include "CopyIn.icc"


// end of file
