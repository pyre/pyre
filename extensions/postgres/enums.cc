// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for the states the server reports, and the layout of the values it sends
void
pyre::postgres::py::enums(py::module & m)
{
    // how a session is doing
    py::enum_<ConnectionStatus>(m, "ConnectionStatus", "whether a session is up")
        // the session is usable
        .value("ok", ConnectionStatus::ok)
        // it is broken beyond repair; only {reset} can help
        .value("bad", ConnectionStatus::bad)
        // libpq is partway through an asynchronous connection, which this package never asks for
        .value("unknown", ConnectionStatus::unknown);

    // how a statement turned out
    py::enum_<ExecStatus>(m, "ExecStatus", "the state the server left a statement in")
        // nothing but whitespace and comments
        .value("emptyQuery", ExecStatus::emptyQuery)
        // it ran, and had no rows to show for it
        .value("commandOk", ExecStatus::commandOk)
        // it ran, and there are rows waiting
        .value("tuplesOk", ExecStatus::tuplesOk)
        // the copy protocol, in each of its three directions
        .value("copyOut", ExecStatus::copyOut)
        .value("copyIn", ExecStatus::copyIn)
        .value("copyBoth", ExecStatus::copyBoth)
        // libpq could not make sense of what came back
        .value("badResponse", ExecStatus::badResponse)
        // it ran, and the server has a warning for us
        .value("nonfatalError", ExecStatus::nonfatalError)
        // it did not run
        .value("fatalError", ExecStatus::fatalError)
        // the piecemeal deliveries of a result set
        .value("singleTuple", ExecStatus::singleTuple)
        .value("chunk", ExecStatus::chunk)
        // and the two that pipelining introduced
        .value("pipelineSync", ExecStatus::pipelineSync)
        .value("pipelineAborted", ExecStatus::pipelineAborted)
        // a status this build of libpq knows and this package does not
        .value("unknown", ExecStatus::unknown);

    // where a session stands with respect to its transaction
    py::enum_<TransactionStatus>(
        m, "TransactionStatus", "where a session stands with respect to its transaction")
        // nothing open
        .value("idle", TransactionStatus::idle)
        // a statement is in flight
        .value("active", TransactionStatus::active)
        // a transaction is open and healthy
        .value("inTransaction", TransactionStatus::inTransaction)
        // a transaction is open, and a statement in it failed; nothing but a rollback will be
        // accepted until it closes
        .value("inError", TransactionStatus::inError)
        // the session itself is broken
        .value("unknown", TransactionStatus::unknown);

    // how the bytes of a value are laid out
    py::enum_<Format>(m, "Format", "whether the bytes of a value are text or its internal form")
        // the text the server's output function produced
        .value("text", Format::text)
        // the internal representation of its type, which postgres neither documents nor keeps
        // stable across its releases
        .value("binary", Format::binary);

    // all done
    return;
}


// end of file
