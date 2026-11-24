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


// verify that a prepared statement runs as often as it is asked, each time with its own arguments
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // teach it a sum of two numbers
    session.prepare("pyre_sum", "SELECT $1::int8 + $2::int4");

    // run it
    const auto first = session.execPrepared("pyre_sum", { "40", "2" });
    // and check the answer
    if (first.value(0, 0) != "42") {
        std::cerr << "40 + 2 came back as " << first.value(0, 0) << std::endl;
        return 1;
    }
    // run it again, with other arguments
    const auto second = session.execPrepared("pyre_sum", { "1", "2" });
    // and check that it used them
    if (second.value(0, 0) != "3") {
        std::cerr << "1 + 2 came back as " << second.value(0, 0) << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
