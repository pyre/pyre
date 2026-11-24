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


// a copy of rows out of the database, from a {COPY … TO STDOUT}
//
// each row arrives as a line of text in the format the statement asked for, which is the text
// format of a copy unless it says otherwise. nothing about the line says what the types of its
// values are, so it is handed back as it arrived
//
// a copy holds the lock of its session from the moment it starts until its last row is out, so
// that no other thread can send a statement that would abandon it; it is used by the thread that
// started it. a copy that goes away before its last row is out ends: outside a transaction, it asks
// the server to stop sending; inside one, where a statement the server stops fails the
// transaction, it reads the rest of the rows and throws them away
//
// a copy may not be copied, because what it started on the server can be ended only once; it
// may be moved, because the obligation to end it can be handed on
class pyre::postgres::CopyOut {
    // types
public:
    // me
    using self_type = CopyOut;
    // the session
    using connection_type = Connection;
    // the hold on the session, which carries the guard of its lock
    using hold_type = Hold;

    // metamethods
public:
    // start the copy {statement}, a {COPY … TO STDOUT}, on {connection}
    explicit inline CopyOut(connection_type connection, view_t statement);
    // what i started on the server can be ended only once, so there is exactly one of me
    CopyOut(const CopyOut &) = delete;
    CopyOut & operator=(const CopyOut &) = delete;
    // but the duty to end it may be passed along
    inline CopyOut(CopyOut && other) noexcept;
    inline CopyOut & operator=(CopyOut && other) noexcept;
    // and whoever ends up holding it ends the copy, unless all the rows are out
    inline ~CopyOut();

    // interface
public:
    // the next row, or nothing once they are all out, which is when a failure of the server is
    // reported
    inline auto next() -> std::optional<string_t>;
    // whether there may be rows still to come
    inline auto live() const -> bool;
    // the statement that started me
    inline auto statement() const -> view_t;

    // implementation details
private:
    // the rows are out: collect the answer of the server, let go of the session, and raise when
    // the server failed
    inline auto _finish() -> void;
    // end the copy and swallow whatever goes wrong; the destructor calls this
    inline auto _close() noexcept -> void;

    // data
private:
    // the session, and my share of it
    connection_type _connection;
    // the hold on the session
    hold_type _hold;
    // the statement that started me
    string_t _statement;
    // whether the session was in a transaction when i started
    bool _transaction;
    // whether there may be rows still to come
    bool _live;
};


// get the inline definitions
#include "CopyOut.icc"


// end of file
