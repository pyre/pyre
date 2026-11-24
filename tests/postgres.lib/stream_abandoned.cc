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


// verify that a stream that goes away before it hands back all its rows leaves the session usable
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());

    // in a scope of its own
    {
        // stream many rows
        auto stream = Stream(session, "SELECT generate_series(1, 1000000)", arguments_t(), 100);
        // take the first batch
        const auto batch = stream.next();
        // which is there
        if (!batch || batch->value(0, 0) != "1") {
            std::cerr << "the first batch did not arrive" << std::endl;
            return 1;
        }
        // and leave without the others
    }

    // the session is free
    if (session.transaction() != TransactionStatus::idle) {
        std::cerr << "the session is not free after an abandoned stream" << std::endl;
        return 1;
    }
    // and usable
    if (session.exec("SELECT 1").value(0, 0) != "1") {
        std::cerr << "the session is not usable after an abandoned stream" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
