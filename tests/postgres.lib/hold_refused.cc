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


// verify that a session in the middle of an answer refuses a hold, as a misuse of the interface
// that names what the hold was for
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // send a statement off, without collecting its answer
    session.send("SELECT 1");

    // attempt to
    try {
        // take a hold on the session
        const auto held = session.hold("a copy");
        // which must fail
        std::cerr << "a session in the middle of an answer was held" << std::endl;
        return 1;
    }
    // as a misuse of the interface
    catch (const InterfaceError & error) {
        // that names what the hold was for
        if (error.diagnostic().command() != "a copy") {
            std::cerr << "the refusal named " << error.diagnostic().command() << std::endl;
            return 1;
        }
    }

    // all done
    return 0;
}


// end of file
