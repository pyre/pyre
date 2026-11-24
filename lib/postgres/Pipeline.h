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
// and i hand back the answers in results
#include "Result.h"
// the answers i expect, in the order i asked for them
#include <deque>


// a pipeline of statements, sent without waiting for the answers to the ones before them
//
// the statements go out as they are given, and their answers come back in the same order, one
// result for each statement, through {next}. a sync marks the end of a segment: the statements of
// a segment run in a transaction of their own, unless they are inside one already, so a statement
// that fails undoes the segment, and the server skips the rest of it, whose results say so; the
// next segment runs. the result of a statement may be read before its segment ends
//
// a pipeline sends without waiting for the socket, and reads the answers that arrive while it
// waits for the one it was asked for, so the server never waits on it while it waits on the
// server, however many statements it sends before it reads
//
// a pipeline holds the lock of its session from the moment it starts until it ends, and the
// session refuses the statements sent around it. a pipeline that goes away before its answers are
// read syncs the statements it sent, reads the answers to the end, and leaves the session as it
// found it. pipelines arrived in libpq 14, and an older one refuses to start them
//
// a pipeline may not be copied, because what it started on the server can be ended only once; it
// may be moved, because the obligation to end it can be handed on
class pyre::postgres::Pipeline {
    // types
public:
    // me
    using self_type = Pipeline;
    // the session
    using connection_type = Connection;
    // the hold on its lock
    using guard_type = Connection::guard_type;
    // how the placeholders of a statement are filled in
    using arguments_type = arguments_t;
    // the answer to a statement
    using result_type = Result;
    // the answers i expect, in order: the statement each one answers, or nothing for a sync
    using expected_type = std::deque<std::optional<string_t>>;

    // metamethods
public:
    // start a pipeline on {connection}
    explicit inline Pipeline(connection_type connection);
    // what i started on the server can be ended only once, so there is exactly one of me
    Pipeline(const Pipeline &) = delete;
    Pipeline & operator=(const Pipeline &) = delete;
    // but the duty to end it may be passed along
    inline Pipeline(Pipeline && other) noexcept;
    inline Pipeline & operator=(Pipeline && other) noexcept;
    // and whoever ends up holding it ends it
    inline ~Pipeline();

    // interface
public:
    // send {statement}, with its placeholders filled in from {arguments}
    inline auto execute(view_t statement, const arguments_type & arguments) -> void;
    // teach the server {statement} under the given {name}
    inline auto prepare(view_t name, view_t statement) -> void;
    // run what the server was taught under {name}, with its placeholders filled in from
    // {arguments}
    inline auto execPrepared(view_t name, const arguments_type & arguments) -> void;
    // end the segment of the statements sent since the last sync
    inline auto sync() -> void;
    // the answer to the next statement, in the order they were sent, or nothing once every
    // statement sent has been answered; a statement that failed, or was skipped, answers with a
    // result that says so
    inline auto next() -> std::optional<result_type>;
    // the number of statements sent whose answers have not been read
    inline auto pending() const -> std::size_t;
    // whether i hold the session
    inline auto live() const -> bool;
    // end me now: sync what was sent, read the answers to the end, and let go of the session
    inline auto close() noexcept -> void;

    // implementation details
private:
    // record that {statement} went out, or complain that it did not, as {status} says
    inline auto _sent(view_t statement, int status) -> void;
    // push out what is waiting to go, and pull in what has arrived, without waiting for either
    inline auto _pump() -> void;
    // the next part of the answers, waiting for the server but never on it
    inline auto _wait() -> PGresult *;
    // the calls into libpq that only a libpq with pipelines has
    inline auto _enter() -> int;
    inline auto _exit() -> int;
    inline auto _sync() -> int;
    inline auto _flush() -> int;

    // data
private:
    // the session, and my share of it
    connection_type _connection;
    // the hold on its lock
    guard_type _guard;
    // the answers i expect, in order
    expected_type _expected;
    // whether statements went out since the last sync
    bool _unsynced;
    // whether the server was asked to send the answers to them
    bool _flushed;
    // whether i hold the session
    bool _live;
};


// get the inline definitions
#include "Pipeline.icc"


// end of file
