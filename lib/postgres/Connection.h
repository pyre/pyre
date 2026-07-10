// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// i own the session
#include "traits.h"
#include "Handle.h"
// i name the states the server reports
#include "status.h"
// i hand back result sets, by value
#include "Result.h"
// and messages from other sessions
#include "Notification.h"
// i turn the arguments of a statement into text
#include "codecs.h"
// and i raise when the server complains
#include "Diagnostic.h"
#include "Error.h"


// a session with the back end
//
// copies of a connection share the session, and the last one to go away closes it. {close}
// hands it back early, and every copy learns that it has: a statement sent through a connection
// that has been closed raises an {InterfaceError}, and does not, as the bindings this package
// replaces used to, hand libpq a pointer to memory it had already freed
class pyre::postgres::Connection {
    // types
public:
    // the opaque pointer libpq uses to name a session
    using handle_type = PGconn *;
    // the shared owner of that pointer
    using storage_type = Handle<ConnectionHandle>;
    // how a session is specified
    using parameters_type = parameters_t;
    // how the placeholders of a statement are filled in
    using arguments_type = arguments_t;

    // metamethods
public:
    // open a session described by {parameters}
    //
    // each parameter is a name and a value, kept apart all the way down to libpq. this is the
    // only way to be sure of what is being sent: a password with a space in it, spliced into a
    // conninfo string, silently becomes a password and a garbage keyword
    explicit inline Connection(const parameters_type & parameters);
    // open a session described by a conninfo string or a postgres uri, for a caller who has one
    // already and knows it is well formed
    explicit inline Connection(view_t conninfo);
    // the full set; copies share the session, moves steal the share
    inline Connection(const Connection &) = default;
    inline Connection(Connection &&) noexcept = default;
    inline Connection & operator=(const Connection &) = default;
    inline Connection & operator=(Connection &&) noexcept = default;
    inline ~Connection() = default;

    // structure
public:
    // the raw pointer, for handing to the libpq c api
    inline auto handle() const -> handle_type;
    // whether the session is up
    inline auto status() const -> ConnectionStatus;
    // the same question, as a predicate
    inline auto ok() const -> bool;
    // contextual conversion to {bool}, true when the session is up and has not been closed
    explicit inline operator bool() const;
    // whatever libpq has to say about the last thing that went wrong, borrowed
    inline auto message() const -> view_t;

    // what the session is
public:
    // the database it is talking to
    inline auto database() const -> view_t;
    // the role it is talking as
    inline auto user() const -> view_t;
    // where the server is
    inline auto host() const -> view_t;
    inline auto port() const -> view_t;
    // the process id of the back end that is serving it, which is what one session needs in
    // order to cancel another
    inline auto backend() const -> int;
    // the descriptor underneath it, for a caller that wants to wait on it
    inline auto socket() const -> int;
    // the version of the wire protocol in use
    inline auto protocol() const -> int;
    // the version of the server, as a number: 16.2 is 160002
    inline auto server() const -> int;
    // where the session stands with respect to its transaction
    inline auto transaction() const -> TransactionStatus;
    // the current value of a server setting, borrowed; empty when the server has not reported
    // this one
    inline auto setting(view_t name) const -> view_t;

    // synchronous execution
public:
    // run {statement} and hand back what the server said
    //
    // this is the one call that accepts more than one statement at a time, separated by
    // semicolons, and it is therefore the one call that must never be handed text a user
    // supplied. the server runs the lot in a single implicit transaction and reports on the
    // last of them
    inline auto exec(view_t statement) const -> Result;

    // run {statement}, with its placeholders filled in from {arguments}
    //
    // the placeholders are spelled {$1}, {$2}, and so on, and they may only stand where a value
    // may stand. the values never become part of the sql, so nothing a caller passes here can
    // change what the statement does
    inline auto execParams(view_t statement, const arguments_type & arguments) const -> Result;

    // the same, with the arguments given as themselves rather than as text
    template <typename... argsT>
    inline auto execute(view_t statement, const argsT &... arguments) const -> Result;

    // teach the server {statement} under the given {name}, so that it need only plan it once
    inline auto prepare(view_t name, view_t statement) const -> void;
    // and run what it was taught
    inline auto execPrepared(view_t name, const arguments_type & arguments) const -> Result;

    // asynchronous execution
    //
    // the four calls below are the pieces the synchronous ones are built out of. unlike them,
    // they do not raise when the server complains: a session that has sent a statement must
    // collect every result the server produces for it before it may send another, and a call
    // that threw partway through the collection would leave the session unusable. so {result}
    // hands back whatever arrived, and it is up to the caller to ask it whether it is {ok},
    // and to call {raise} on it when it is not
public:
    // send {statement} off, and do not wait for it
    inline auto send(view_t statement) const -> void;
    // the same, with placeholders
    inline auto sendParams(view_t statement, const arguments_type & arguments) const -> void;
    // read whatever the server has sent us so far; this is what makes {busy} worth asking, and
    // a loop that asks {busy} without ever calling this one never ends
    inline auto consume() const -> void;
    // whether the answer to the statement in flight is still incomplete
    inline auto busy() const -> bool;
    // the next result the server produced, or nothing when it has produced them all; a caller
    // that stops before this hands back nothing has left the session mid-answer
    inline auto result() const -> std::optional<Result>;

    // ask the server to give up on the statement in flight
    inline auto cancel() const -> void;
    // whether the calls that send do so without waiting for the socket to drain
    inline auto nonblocking(bool state) const -> void;
    // push whatever is queued out to the server; zero when it all went, one when some of it is
    // still waiting for a socket that is not ready
    inline auto flush() const -> int;

    // messages from other sessions
public:
    // the next message this session has collected, or nothing. messages arrive on the back of
    // ordinary traffic, so a session that is asking and never sending calls {consume} first
    inline auto notification() const -> std::optional<Notification>;

    // quoting
    //
    // these two are the reason a connection has to be involved in quoting at all: what needs
    // escaping depends on the encoding the session negotiated with the server, and on whether
    // that server treats a backslash as an escape
public:
    // wrap {text} in quotes, and escape whatever inside it needs escaping, so that the result
    // may stand where a literal may stand
    inline auto escapeLiteral(view_t text) const -> string_t;
    // the same, for a name that must stand where an identifier may stand
    inline auto escapeIdentifier(view_t name) const -> string_t;

    // lifecycle
public:
    // close the session and open a new one with the same parameters; this is the only way back
    // from a session whose status has gone bad
    inline auto reset() const -> void;
    // hand the session back now, rather than when the last copy of me goes away. every copy
    // observes this, and refuses to be used afterwards
    inline auto close() -> void;

    // implementation details
private:
    // the raw pointer, checked; everything that talks to libpq goes through here
    inline auto _handle() const -> handle_type;
    // adopt the result libpq produced for {statement}, and raise unless the server ran it
    inline auto _harvest(PGresult * result, view_t statement) const -> Result;
    // build the arrays libpq wants and hand them to whichever of its calls the caller meant
    inline auto _exec(view_t statement, const arguments_type & arguments, bool prepared) const
        -> PGresult *;
    // complain that libpq gave up before the server ever heard of {statement}
    [[noreturn]] inline auto _fail(view_t statement) const -> void;
    // open a session; a failure here has no session to hang a diagnostic off, so it is the one
    // place that must clean up after itself before it throws
    static inline auto _connect(const parameters_type & parameters) -> handle_type;
    static inline auto _connect(view_t conninfo) -> handle_type;
    // and the check the two of them share
    static inline auto _established(handle_type connection) -> handle_type;

    // data
private:
    // the session, and my share of it
    storage_type _connection;
};


// get the inline definitions
#include "Connection.icc"


// end of file
