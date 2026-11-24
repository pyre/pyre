// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// i hold a share of the session i run on
#include "Connection.h"


// the scope of a transaction, tied to the lifetime of an object
//
// a transaction opens as it is built and rolls back as it is destroyed, unless somebody committed
// it first. this is the only way to be sure that a statement that threw does not leave a
// transaction open behind it: the stack unwinds, the destructor runs, and the server hears about
// it whether or not the caller remembered to say so
//
// a transaction opened while the session is already in one is a savepoint inside it: committing
// it keeps its work for the transaction around it to decide on, and rolling it back undoes only
// its own work
//
// a transaction may not be copied, because what it opened on the server can be closed only
// once; it may be moved, because the obligation to close it can be handed on
class pyre::postgres::Transaction {
    // types
public:
    // me
    using self_type = Transaction;
    using connection_type = Connection;

    // metamethods
public:
    // open a transaction on {connection}, or a savepoint when it is in one already
    explicit inline Transaction(connection_type connection);
    // what i opened on the server can be closed only once, so there is exactly one of me
    Transaction(const Transaction &) = delete;
    Transaction & operator=(const Transaction &) = delete;
    // but the duty to close it may be passed along
    inline Transaction(Transaction && other) noexcept;
    inline Transaction & operator=(Transaction && other) noexcept;
    // and whoever ends up holding it closes it
    inline ~Transaction();

    // interface
public:
    // make everything done inside me permanent
    inline auto commit() -> void;
    // and undo it instead
    inline auto rollback() -> void;
    // whether i am still open, i.e. whether neither of the two above has been called
    inline auto live() const -> bool;

    // the session i run on, for a caller that has only me to hand
    inline auto connection() const -> const connection_type &;

    // implementation details
private:
    // close me, one way or the other, and swallow whatever goes wrong; the destructor calls
    // this, and a destructor that throws during unwinding takes the process with it
    inline auto _close() noexcept -> void;

    // data
private:
    // the session, and my share of it
    connection_type _connection;
    // the name of my savepoint, when i was opened inside a transaction; empty otherwise
    string_t _savepoint;
    // whether the transaction is still open
    bool _live;
    // the number of savepoints set so far in this process, which names the next one, so that
    // the names are unique within every session
    inline static std::atomic<long> _savepoints = 0;
};


// get the inline definitions
#include "Transaction.icc"


// end of file
