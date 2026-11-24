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


// verify that asking for the description of a name the session was never taught is refused
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());

    // attempt to
    try {
        // describe a statement nobody prepared
        session.describe("pyre_nothing");
        // which must fail
        std::cerr << "a name nobody prepared was described" << std::endl;
        return 1;
    }
    // the way the server reports a missing prepared statement
    catch (const OperationalError & error) {
        // with its own code for it
        if (error.diagnostic().sqlstate() != "26000") {
            std::cerr << "the refusal carried " << error.diagnostic().sqlstate() << std::endl;
            return 1;
        }
        // and the name the caller used
        if (error.diagnostic().command() != "pyre_nothing") {
            std::cerr << "the refusal named " << error.diagnostic().command() << std::endl;
            return 1;
        }
    }

    // all done
    return 0;
}


// end of file
