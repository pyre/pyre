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
// and i hand back the rows in results
#include "Result.h"


// the rows of a selection, read in batches as the server sends them
//
// the server sends the rows as it makes them, and libpq hands them over in batches of the size
// the stream asks for; a libpq older than 17 hands them over one at a time. the batches are
// results whose rows are the next few of the selection. the answer is over when {next} hands
// back nothing, which is when a failure of the server is reported, as the condition it named;
// the rows that came before the failure have been handed back already
//
// a stream holds the lock of its session from the moment it starts until its last row is read,
// so that no other thread can send a statement in the meantime, and the session refuses the
// statements its own thread sends. a stream that goes away before its last row is read stops
// the answer: outside a transaction, it asks the server to stop sending; inside one, where a
// statement the server stops fails the transaction, it reads the rest of the rows and throws
// them away
//
// a stream may not be copied, because what it started on the server can be ended only once; it
// may be moved, because the obligation to end it can be handed on
class pyre::postgres::Stream {
    // types
public:
    // me
    using self_type = Stream;
    // the session
    using connection_type = Connection;
    // the hold on the session, which carries the guard of its lock
    using hold_type = Hold;
    // how the placeholders of the statement are filled in
    using arguments_type = arguments_t;
    // a batch of rows
    using result_type = Result;

    // metamethods
public:
    // start {statement} on {connection}, with its placeholders filled in from {arguments}, and
    // ask for its rows {batch} at a time
    inline Stream(
        connection_type connection, view_t statement, const arguments_type & arguments, int batch);
    // what i started on the server can be ended only once, so there is exactly one of me
    Stream(const Stream &) = delete;
    Stream & operator=(const Stream &) = delete;
    // but the duty to end it may be passed along
    inline Stream(Stream && other) noexcept;
    inline Stream & operator=(Stream && other) noexcept;
    // and whoever ends up holding it stops the answer, unless all the rows are read
    inline ~Stream();

    // interface
public:
    // the next batch of rows, or nothing once they are all read, which is when a failure of the
    // server is reported
    inline auto next() -> std::optional<result_type>;
    // whether there may be rows still to come
    inline auto live() const -> bool;
    // the statement that started me
    inline auto statement() const -> view_t;
    // the number of rows i asked for in each batch
    inline auto batch() const -> int;

    // implementation details
private:
    // the answer is over: let go of the session
    inline auto _end() -> void;
    // stop the answer and swallow whatever goes wrong; the destructor calls this
    inline auto _close() noexcept -> void;

    // data
private:
    // the session, and my share of it
    connection_type _connection;
    // the hold on the session
    hold_type _hold;
    // the statement that started me
    string_t _statement;
    // the number of rows in a batch
    int _batch;
    // whether the session was in a transaction when i started
    bool _transaction;
    // whether there may be rows still to come
    bool _live;
};


// get the inline definitions
#include "Stream.icc"


// end of file
