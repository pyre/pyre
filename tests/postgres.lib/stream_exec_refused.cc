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


// verify that a statement sent through a session in the middle of a stream is refused as a misuse
// of the interface, and that the stream hands back the rest of its rows
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // stream five rows, two at a time
    auto stream = Stream(session, "SELECT generate_series(1, 5)", arguments_t(), 2);
    // take the first batch
    const auto first = stream.next();
    // which is there
    if (!first) {
        std::cerr << "the first batch did not arrive" << std::endl;
        return 1;
    }
    // count its rows
    auto rows = first->rows();

    // attempt to
    try {
        // send another statement in the middle of the stream
        session.exec("SELECT 42");
        // which must fail
        std::cerr << "a statement sent in the middle of a stream was accepted" << std::endl;
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

    // the stream hands back the rest of its rows
    while (const auto batch = stream.next()) {
        // count them
        rows += batch->rows();
    }
    // all of them
    if (rows != 5) {
        std::cerr << "the stream handed back " << rows << " rows, not 5" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
