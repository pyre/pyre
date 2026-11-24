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


// verify that a copy into the database sent as an ordinary statement is refused as a misuse of
// the interface, rather than leaving the session waiting for rows, and that the session is usable
// afterwards
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec("CREATE TEMPORARY TABLE pyre_copy (id integer)");

    // attempt to
    try {
        // send the copy as an ordinary statement
        session.exec("COPY pyre_copy FROM STDIN");
        // which must fail
        std::cerr << "a copy sent as an ordinary statement was accepted" << std::endl;
        return 1;
    }
    // as a misuse of the interface
    catch (const InterfaceError & error) {
        // that names the statement
        if (error.diagnostic().command() != "COPY pyre_copy FROM STDIN") {
            std::cerr << "the refusal named " << error.diagnostic().command() << std::endl;
            return 1;
        }
    }

    // the session is no longer in the copy
    if (session.transaction() != TransactionStatus::idle) {
        std::cerr << "the session was left in the copy" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
