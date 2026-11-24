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


// verify that a statement sent through a session whose answer to an earlier one has not been
// collected is refused as a misuse of the interface, and that the answer is still there to collect
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // send a statement off, without waiting for its answer
    session.send("SELECT generate_series(1, 3)");

    // attempt to
    try {
        // send another before collecting it
        session.exec("SELECT 42");
        // which must fail
        std::cerr << "a statement sent before the answer to another was accepted" << std::endl;
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

    // the answer is still there
    const auto answer = session.result();
    // with its rows
    if (!answer || answer->rows() != 3) {
        std::cerr << "the answer to the first statement was lost" << std::endl;
        return 1;
    }
    // and nothing after it
    if (session.result()) {
        std::cerr << "the session had more to say" << std::endl;
        return 1;
    }

    // the session is usable
    if (session.exec("SELECT 1").value(0, 0) != "1") {
        std::cerr << "the session is not usable after collecting the answer" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
