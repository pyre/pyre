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


// verify that a copy that goes away before it is finished keeps none of its rows, and leaves the
// session usable
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec("CREATE TEMPORARY TABLE pyre_copy (id integer)");

    // in a scope of its own
    {
        // start a copy
        auto copy = CopyIn(session, "COPY pyre_copy FROM STDIN");
        // send a row
        copy.record(1);
        // and leave without finishing it
    }

    // the table is empty
    const auto rows = session.exec("SELECT count(*) FROM pyre_copy");
    // so say
    if (rows.value(0, 0) != "0") {
        std::cerr << "an abandoned copy kept " << rows.value(0, 0) << " rows" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
