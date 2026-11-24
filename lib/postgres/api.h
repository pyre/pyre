// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// externals
#include "external.h"
// forward declarations
#include "forward.h"


// the canonical names for the pyre-owned wrappers over the postgres client library
namespace pyre::postgres {
    // the exception hierarchy
    using exception_t = Exception;
    using warning_t = Warning;
    using error_t = Error;
    using interfaceError_t = InterfaceError;
    using databaseError_t = DatabaseError;
    using dataError_t = DataError;
    using operationalError_t = OperationalError;
    using integrityError_t = IntegrityError;
    using internalError_t = InternalError;
    using programmingError_t = ProgrammingError;
    using notSupportedError_t = NotSupportedError;

    // what the server says about a statement that did not work out
    using diagnostic_t = Diagnostic;

    // what it sends back when one does
    using field_t = Field;
    using row_t = Row;
    using result_t = Result;

    // the session, the hold on it for the length of an answer, and the scope of the work done
    // over it
    using connection_t = Connection;
    using hold_t = Hold;
    using transaction_t = Transaction;
    // the copies of rows into a table and out of the database
    using copyIn_t = CopyIn;
    using copyOut_t = CopyOut;
    // the rows of a selection, read in batches as the server sends them
    using stream_t = Stream;
    // a pipeline of statements, sent without waiting for the answers to the ones before them
    using pipeline_t = Pipeline;
    // and what other sessions have to say
    using notification_t = Notification;

    // the states the server reports
    using connectionStatus_t = ConnectionStatus;
    using execStatus_t = ExecStatus;
    using transactionStatus_t = TransactionStatus;
    // and the layout of the values it sends
    using format_t = Format;
} // namespace pyre::postgres


// end of file
