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


// verify that a name the session has prepared already is refused as a mistake in the statement
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // teach it a statement
    session.prepare("pyre_one", "SELECT 1");

    // attempt to
    try {
        // teach it another under the same name
        session.prepare("pyre_one", "SELECT 2");
        // which must fail
        std::cerr << "a name was prepared twice" << std::endl;
        return 1;
    }
    // as a mistake in the statement
    catch (const ProgrammingError & error) {
        // that the server calls a duplicate prepared statement
        if (error.diagnostic().sqlstate() != "42P05") {
            std::cerr << "the refusal carried " << error.diagnostic().sqlstate() << std::endl;
            return 1;
        }
    }

    // the first statement is still there
    if (session.execPrepared("pyre_one", {}).value(0, 0) != "1") {
        std::cerr << "the refusal changed the statement that was there" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
