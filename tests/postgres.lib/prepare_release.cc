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


// verify that a released statement is gone, and that its name is free to be used again
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // teach it a statement
    session.prepare("pyre_one", "SELECT 1");
    // and make it forget
    session.release("pyre_one");

    // attempt to
    try {
        // run what it forgot
        session.execPrepared("pyre_one", {});
        // which must fail
        std::cerr << "a released statement ran" << std::endl;
        return 1;
    }
    // the way the server reports a missing prepared statement
    catch (const OperationalError & error) {
        // with its own code for it
        if (error.diagnostic().sqlstate() != "26000") {
            std::cerr << "the refusal carried " << error.diagnostic().sqlstate() << std::endl;
            return 1;
        }
    }

    // the name is free, so teach it another statement under it
    session.prepare("pyre_one", "SELECT 2");
    // which is the one that runs
    if (session.execPrepared("pyre_one", {}).value(0, 0) != "2") {
        std::cerr << "the name did not take the new statement" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
