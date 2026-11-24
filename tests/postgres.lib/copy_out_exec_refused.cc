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


// verify that a statement sent through a session in the middle of a copy out of the database is
// refused as a misuse of the interface, and that the copy hands back the rest of its rows
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // start a copy of five rows
    auto copy = CopyOut(session, "COPY (SELECT generate_series(1, 5)) TO STDOUT");
    // take the first
    const auto first = copy.next();
    // which is there
    if (!first || *first != "1\n") {
        std::cerr << "the first row did not come out" << std::endl;
        return 1;
    }

    // attempt to
    try {
        // send another statement in the middle of the copy
        session.exec("SELECT 42");
        // which must fail
        std::cerr << "a statement sent in the middle of a copy was accepted" << std::endl;
        return 1;
    }
    // as a misuse of the interface
    catch (const InterfaceError & error) {
        // that names the statement
        if (error.diagnostic().command() != "SELECT 42") {
            std::cerr << "the refusal named " << error.diagnostic().command() << std::endl;
            return 1;
        }
    }

    // the copy hands back the rest of its rows
    auto rows = 1;
    // go through them
    while (copy.next()) {
        // and count them
        ++rows;
    }
    // all of them
    if (rows != 5) {
        std::cerr << "the copy handed back " << rows << " rows, not 5" << std::endl;
        return 1;
    }

    // and the session is usable
    if (session.exec("SELECT 1").value(0, 0) != "1") {
        std::cerr << "the session is not usable after the copy" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
