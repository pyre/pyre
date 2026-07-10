// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the definitions of the translators that turn the answers of libpq into my labels
//
// every one of them has a fallback, and every fallback trips a firewall: a status this package
// does not recognize means libpq has grown one since this file was written, and the code must
// change. the old bindings had no such backstop, and quietly reported half of what the server
// said as a syntax error


// how a session is doing
auto
pyre::postgres::connectionStatus(ConnStatusType status) -> ConnectionStatus
{
    // a session that libpq is willing to talk to
    if (status == CONNECTION_OK) {
        return ConnectionStatus::ok;
    }
    // one that it is not
    if (status == CONNECTION_BAD) {
        return ConnectionStatus::bad;
    }

    // everything else is one of the intermediate states of an asynchronous connection. this
    // package always connects synchronously, so seeing one here is not an error, just an answer
    // we have no use for
    return ConnectionStatus::unknown;
}


// how a statement turned out
auto
pyre::postgres::execStatus(ExecStatusType status) -> ExecStatus
{
    // walk through the states libpq has had since forever
    switch (status) {
        // nothing but whitespace and comments
        case PGRES_EMPTY_QUERY:
            return ExecStatus::emptyQuery;
        // it ran, and had no rows to show for it
        case PGRES_COMMAND_OK:
            return ExecStatus::commandOk;
        // it ran, and there are rows waiting
        case PGRES_TUPLES_OK:
            return ExecStatus::tuplesOk;
        // the server is about to stream a table at us
        case PGRES_COPY_OUT:
            return ExecStatus::copyOut;
        // the server is waiting for us to stream a table at it
        case PGRES_COPY_IN:
            return ExecStatus::copyIn;
        // both directions at once, which is what replication looks like
        case PGRES_COPY_BOTH:
            return ExecStatus::copyBoth;
        // libpq could not make sense of what came back
        case PGRES_BAD_RESPONSE:
            return ExecStatus::badResponse;
        // the statement ran, and the server has a warning for us
        case PGRES_NONFATAL_ERROR:
            return ExecStatus::nonfatalError;
        // the statement did not run
        case PGRES_FATAL_ERROR:
            return ExecStatus::fatalError;
        // one row of a set being delivered a row at a time
        case PGRES_SINGLE_TUPLE:
            return ExecStatus::singleTuple;

// the chunked delivery of a result set arrived in libpq 17, and it announces itself
#if defined(LIBPQ_HAS_CHUNK_MODE)
        // one batch of a set being delivered in chunks
        case PGRES_TUPLES_CHUNK:
            return ExecStatus::chunk;
#endif

// pipelining arrived in libpq 14, and it too announces itself
#if defined(LIBPQ_HAS_PIPELINING)
        // the boundary between two batches
        case PGRES_PIPELINE_SYNC:
            return ExecStatus::pipelineSync;
        // a statement that never ran because one ahead of it in the pipeline failed
        case PGRES_PIPELINE_ABORTED:
            return ExecStatus::pipelineAborted;
#endif

        // and anything else
        default:
            break;
    }

    // a status we have no name for means libpq has moved on without us
    auto channel = pyre::journal::firewall_t("pyre.postgres.status");
    // so complain
    channel
        // what
        << "unknown result status"
        << pyre::journal::newline
        // details
        << "libpq reported " << static_cast<int>(status)
        // where, and flush
        << pyre::journal::endl(__HERE__);

    // in a build with firewalls disabled, say that we do not know
    return ExecStatus::unknown;
}


// whether a statement that ended in this state ran at all
auto
pyre::postgres::succeeded(ExecStatus status) -> bool
{
    // the states in which the server did what it was asked
    switch (status) {
        // an empty statement is a statement that ran, trivially
        case ExecStatus::emptyQuery:
        // it ran, with or without rows to show for it
        case ExecStatus::commandOk:
        case ExecStatus::tuplesOk:
        // the copy protocol is under way, which is what the caller asked for
        case ExecStatus::copyOut:
        case ExecStatus::copyIn:
        case ExecStatus::copyBoth:
        // a row, or a chunk of rows, off a stream that is still running
        case ExecStatus::singleTuple:
        case ExecStatus::chunk:
        // the end of a pipelined batch
        case ExecStatus::pipelineSync:
            return true;
        // a warning means the statement ran; the caller may still want to hear about it, but
        // that is a decision for whoever built the result, not for this predicate
        case ExecStatus::nonfatalError:
            return true;
        // and everything else means it did not
        default:
            return false;
    }
}


// render one of my labels as text
auto
pyre::postgres::describe(ExecStatus status) -> view_t
{
    // spell out each one
    switch (status) {
        case ExecStatus::emptyQuery:
            return "the statement was empty";
        case ExecStatus::commandOk:
            return "the statement ran and returned no rows";
        case ExecStatus::tuplesOk:
            return "the statement ran and returned rows";
        case ExecStatus::copyOut:
            return "the server is sending the contents of a table";
        case ExecStatus::copyIn:
            return "the server is receiving the contents of a table";
        case ExecStatus::copyBoth:
            return "the server is both sending and receiving table contents";
        case ExecStatus::badResponse:
            return "the server sent something libpq could not understand";
        case ExecStatus::nonfatalError:
            return "the statement ran, and the server issued a warning";
        case ExecStatus::fatalError:
            return "the statement did not run";
        case ExecStatus::singleTuple:
            return "one row of a result set delivered a row at a time";
        case ExecStatus::chunk:
            return "one chunk of a result set delivered in batches";
        case ExecStatus::pipelineSync:
            return "the boundary between two pipelined batches";
        case ExecStatus::pipelineAborted:
            return "the statement was skipped because an earlier one in its pipeline failed";
        case ExecStatus::unknown:
            return "the statement ended in a state this package does not recognize";
    }

    // an enumerator with no case above is a bug in this function
    auto channel = pyre::journal::firewall_t("pyre.postgres.status");
    // so complain
    channel
        // what
        << "no description for result status " << static_cast<int>(status)
        // where, and flush
        << pyre::journal::endl(__HERE__);

    // and say nothing
    return "";
}


// where a session stands with respect to its transaction
auto
pyre::postgres::transactionStatus(PGTransactionStatusType status) -> TransactionStatus
{
    // walk through the five answers libpq has
    switch (status) {
        // nothing open
        case PQTRANS_IDLE:
            return TransactionStatus::idle;
        // a statement is in flight
        case PQTRANS_ACTIVE:
            return TransactionStatus::active;
        // a transaction is open and healthy
        case PQTRANS_INTRANS:
            return TransactionStatus::inTransaction;
        // a transaction is open, and something in it went wrong
        case PQTRANS_INERROR:
            return TransactionStatus::inError;
        // the session itself is broken
        case PQTRANS_UNKNOWN:
            return TransactionStatus::unknown;
    }

    // as everywhere else, a status with no label is a bug
    auto channel = pyre::journal::firewall_t("pyre.postgres.status");
    // so complain
    channel
        // what
        << "unknown transaction status"
        << pyre::journal::newline
        // details
        << "libpq reported " << static_cast<int>(status)
        // where, and flush
        << pyre::journal::endl(__HERE__);

    // and fall back on the answer that promises nothing
    return TransactionStatus::unknown;
}


// how the bytes of a value are laid out
auto
pyre::postgres::format(int code) -> Format
{
    // text
    if (code == 0) {
        return Format::text;
    }
    // binary
    if (code == 1) {
        return Format::binary;
    }

    // the wire protocol has room for more, but has never used it
    auto channel = pyre::journal::firewall_t("pyre.postgres.status");
    // so complain
    channel
        // what
        << "unknown column format"
        << pyre::journal::newline
        // details
        << "libpq reported " << code
        // where, and flush
        << pyre::journal::endl(__HERE__);

    // and assume the value is text, which is what every server has ever sent unless asked
    return Format::text;
}


// end of file
