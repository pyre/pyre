// -*- C++ -*-
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

    // the session, and the scope of the work done over it
    using connection_t = Connection;
    using transaction_t = Transaction;
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
