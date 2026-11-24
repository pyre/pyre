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


// verify that the rows sent through a copy land in the table, each value in its column, and that
// the server counts them
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec("CREATE TEMPORARY TABLE pyre_copy (id integer, name text)");

    // start a copy into it
    auto copy = CopyIn(session, "COPY pyre_copy (id, name) FROM STDIN");
    // send two rows, built out of c++ values
    copy.record(1, string_t("one"));
    copy.record(2, string_t("two"));
    // and finish
    const auto result = copy.end();

    // the server counted the rows
    if (result.affected() != 2) {
        std::cerr << "the copy reported " << result.affected() << " rows" << std::endl;
        return 1;
    }

    // read them back
    const auto rows = session.exec("SELECT id, name FROM pyre_copy ORDER BY id");
    // both are there
    if (rows.rows() != 2) {
        std::cerr << "the table holds " << rows.rows() << " rows" << std::endl;
        return 1;
    }
    // with their values
    if (rows.value(0, 0) != "1" || rows.value(0, 1) != "one" || rows.value(1, 0) != "2"
        || rows.value(1, 1) != "two") {
        std::cerr << "the rows came back with other values" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
