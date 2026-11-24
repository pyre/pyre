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


// verify that a hold knows when its session has been closed, and refuses to hand over the
// pointer to it
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    auto session = Connection(specification());
    // take a hold on it
    auto held = session.hold("a hold");
    // close the session, from the thread that holds it
    session.close();

    // the hold knows
    if (held.open()) {
        std::cerr << "the hold thinks a closed session is open" << std::endl;
        return 1;
    }
    // attempt to
    try {
        // get the pointer to the session
        held.handle();
        // which must fail
        std::cerr << "the hold handed over the pointer to a closed session" << std::endl;
        return 1;
    }
    // as a misuse of the interface
    catch (const InterfaceError & error) {
        // which is what is expected
        held.release();
    }

    // all done
    return 0;
}


// end of file
