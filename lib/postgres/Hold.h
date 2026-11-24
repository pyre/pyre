// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// i hold a share of the session
#include "traits.h"
#include "Handle.h"
// i name the states the server reports
#include "status.h"
// and i raise when the session fails
#include "Diagnostic.h"
#include "Error.h"
// the lock of the session
#include <mutex>


// the hold on a session for the length of an answer
//
// a hold is handed out by {Connection::hold}, which takes the lock of the session and refuses a
// session that is in the middle of an answer, or in a pipeline. it carries a share of the session
// and the guard of its lock, and lets its owner talk to libpq through the session for as long as
// the answer lasts: the copies, the streams and the pipelines hold one from the moment they start
// until they end. the other threads that share the session wait for it, and the thread that holds
// it may call the session as it pleases
//
// a hold may not be copied, since there is one lock to let go of; it may be moved, along with the
// duty to let go of it
class pyre::postgres::Hold {
    // types
public:
    // me
    using self_type = Hold;
    // the opaque pointer libpq uses to name a session
    using handle_type = PGconn *;
    // the shared owner of that pointer
    using storage_type = Handle<ConnectionHandle>;
    // the guard of the lock of the session
    using guard_type = std::unique_lock<std::recursive_mutex>;
    // how the placeholders of a statement are filled in
    using arguments_type = arguments_t;

    // metamethods
public:
    // hold {session}, whose lock {guard} holds
    inline Hold(storage_type session, guard_type guard);
    // there is one lock to let go of, so there is exactly one of me
    Hold(const Hold &) = delete;
    Hold & operator=(const Hold &) = delete;
    // but the duty to let go of it may be passed along
    Hold(Hold &&) noexcept = default;
    Hold & operator=(Hold &&) noexcept = default;
    // and whoever ends up with it lets go of the lock
    ~Hold() = default;

    // interface
public:
    // the raw pointer to the session, for handing to the libpq c api; a session that has been
    // closed is refused
    inline auto handle() const -> handle_type;
    // whether the session is still open
    inline auto open() const -> bool;
    // whether i still hold the lock
    inline auto held() const -> bool;
    // let go of the lock
    inline auto release() -> void;

    // talking to libpq
public:
    // send {statement}, or run the prepared statement it names when {prepared}, with its
    // placeholders filled in from {arguments}, without waiting; zero means nothing went
    inline auto send(view_t statement, const arguments_type & arguments, bool prepared) const
        -> int;
    // complain that libpq gave up before the server ever heard of {statement}
    [[noreturn]] inline auto fail(view_t statement) const -> void;
    // end the copy the server is in, as {status} says, giving {reason} for rows that will not
    // come, and collect the rest of its answer; this cleans up after a failure, so it swallows
    // whatever goes wrong
    inline auto abandon(ExecStatus status, view_t reason) const noexcept -> void;
    // refuse {statement}, a {COPY} sent through a call that cannot move its rows, once the copy
    // it started is ended
    [[noreturn]] inline auto refuse(ExecStatus status, view_t statement) const -> void;

    // data
private:
    // my share of the session
    storage_type _session;
    // and the guard of its lock
    guard_type _guard;
};


// get the inline definitions
#include "Hold.icc"


// end of file
