// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>

// the package under test
#include <pyre/postgres.h>
// support
#include <pyre/journal.h>
// so a failing test can say why
#include <iostream>


// the session this suite runs on
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// verify that a stream asked for batches of no rows is refused as a misuse of the interface before
// its statement is sent, and that the session is free afterwards
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // the statement
    const string_t statement = "SELECT generate_series(1, 5)";

    // attempt to
    try {
        // stream it in batches of no rows
        const auto stream = Stream(session, statement, arguments_t(), 0);
        // which must fail
        std::cerr << "a stream in batches of " << stream.batch() << " rows was accepted"
                  << std::endl;
        return 1;
    }
    // as a misuse of the interface
    catch (const InterfaceError & error) {
        // that names the statement
        if (error.diagnostic().command() != statement) {
            std::cerr << "the refusal named " << error.diagnostic().command() << std::endl;
            return 1;
        }
    }

    // the session is free
    if (session.transaction() != TransactionStatus::idle) {
        std::cerr << "the session is not free after the refusal" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
