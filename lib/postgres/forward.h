// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external packages and the type aliases that shape this namespace
#include "external.h"


// the pyre-owned wrappers over the postgres client library
namespace pyre::postgres {
    // the exception hierarchy
    // the base of everything this package throws
    class Exception;
    // something the back end wants us to know about, but that did not stop it
    class Warning;
    // the base of everything that did stop it
    class Error;
    // a mistake made on this side of the wire, before the back end ever saw the statement
    class InterfaceError;
    // a complaint that came back from the server
    class DatabaseError;
    // the data in the statement was wrong; a number that does not parse, a date that does not
    // exist
    class DataError;
    // the environment failed us; the connection dropped, the disk filled up, the server died
    class OperationalError;
    // the statement would have left the database inconsistent
    class IntegrityError;
    // the back end found itself in a state it does not believe in
    class InternalError;
    // the statement was malformed; a syntax error, an unknown table, the wrong column count
    class ProgrammingError;
    // the statement asked for something this server cannot do
    class NotSupportedError;

    // everything the server has to say about a statement that did not work out
    class Diagnostic;

    // the owner of a libpq object
    template <class traitsT>
    class Handle;
    // the recipes that teach {Handle} how to release each kind of libpq object
    struct ConnectionHandle;
    struct ResultHandle;

    // one value in a result set, together with what its column says it means
    class Field;
    // one row of a result set
    class Row;
    // everything the server sent back in answer to one statement
    class Result;

    // a session with the back end
    class Connection;
    // the scope of a transaction, tied to the lifetime of an object
    class Transaction;
    // an asynchronous message from another session
    struct Notification;
} // namespace pyre::postgres


// how a session is doing
namespace pyre::postgres {
    enum class ConnectionStatus {
        // the session is up and usable
        ok,
        // the session is broken beyond repair; only {reset} can help
        bad,
        // libpq is partway through establishing an asynchronous connection, which is a mode
        // this package does not offer; the label exists so that no answer goes unnamed
        unknown,
    };

    // translate the answer of {PQstatus} into one of my labels
    inline auto connectionStatus(ConnStatusType status) -> ConnectionStatus;
} // namespace pyre::postgres


// how a statement turned out
namespace pyre::postgres {
    enum class ExecStatus {
        // the statement was empty, or was nothing but a comment
        emptyQuery,
        // the statement ran and returned no rows
        commandOk,
        // the statement ran and returned rows
        tuplesOk,
        // the server is ready to send us the contents of a table
        copyOut,
        // the server is ready to receive the contents of a table
        copyIn,
        // both at once, which is how replication talks
        copyBoth,
        // the server said something libpq could not understand
        badResponse,
        // a warning; the statement ran
        nonfatalError,
        // the statement did not run
        fatalError,
        // one row of a result set being delivered a row at a time
        singleTuple,
        // one batch of a result set being delivered in chunks; libpq 17 and later
        chunk,
        // the boundary between two pipelined batches; libpq 14 and later
        pipelineSync,
        // the statement was skipped because an earlier one in its pipeline failed
        pipelineAborted,
        // a status this build of libpq knows and this package does not
        unknown,
    };

    // translate the answer of {PQresultStatus} into one of my labels
    inline auto execStatus(ExecStatusType status) -> ExecStatus;
    // whether a statement that ended in this state ran at all
    inline auto succeeded(ExecStatus status) -> bool;
    // render one of my labels as text, for the benefit of a diagnostic
    inline auto describe(ExecStatus status) -> view_t;
} // namespace pyre::postgres


// where a session stands with respect to its transaction
namespace pyre::postgres {
    enum class TransactionStatus {
        // no transaction is open
        idle,
        // a statement is in flight
        active,
        // a transaction is open and healthy
        inTransaction,
        // a transaction is open, and a statement in it failed; nothing but a rollback will be
        // accepted until it closes
        inError,
        // the session is broken, so there is nothing to report
        unknown,
    };

    // translate the answer of {PQtransactionStatus} into one of my labels
    inline auto transactionStatus(PGTransactionStatusType status) -> TransactionStatus;
} // namespace pyre::postgres


// how the bytes of a value are laid out
namespace pyre::postgres {
    // the two spellings libpq understands; the values are fixed by the wire protocol, so they
    // are written out rather than left to the compiler
    enum class Format {
        // the value is the text the server's output function produced
        text = 0,
        // the value is the internal representation of its type, in network byte order
        binary = 1,
    };

    // translate the answer of {PQfformat} into one of my labels
    inline auto format(int code) -> Format;
} // namespace pyre::postgres


// the translation of a server complaint into an exception
namespace pyre::postgres {
    // work out which of my exceptions {diagnostic} describes, and throw it. the choice is made
    // by the SQLSTATE the server sent, which is the only part of a complaint that is portable;
    // its message is written for a human, and in whatever language the server was configured
    // to speak
    [[noreturn]] inline auto raise(Diagnostic diagnostic) -> void;
} // namespace pyre::postgres


// the translation between the values of a c++ program and the text postgres exchanges
namespace pyre::postgres {
    // the recipe for moving values of type {valueT} across the wire
    //
    // this is the extension point of the package: a client with a type of its own specializes
    // this template, and its type is thereafter accepted by {Connection::execute} and handed
    // back by {Field::as}, with no further cooperation from anybody here. the specializations
    // in {codecs.h} cover the types postgres and c++ already agree about
    //
    // the second parameter is what lets a specialization claim a whole family of types at once,
    // e.g. every integral type, through {std::enable_if}; callers never mention it
    template <typename valueT, typename enableT = void>
    struct Codec;

    // turn the text in {value} into a {valueT}
    template <typename valueT>
    inline auto decode(view_t value) -> valueT;
    // turn {value} into the text postgres expects, or into {NULL}
    template <typename valueT>
    inline auto encode(const valueT & value) -> argument_t;
} // namespace pyre::postgres


// end of file
