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


// verify that a row the server refuses is reported when the copy ends, as the condition the
// server named, and that the session is usable afterwards
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec("CREATE TEMPORARY TABLE pyre_copy (id integer)");

    // start a copy into it
    auto copy = CopyIn(session, "COPY pyre_copy FROM STDIN");
    // send a row that is not an integer
    copy.record(string_t("not a number"));
    // attempt to
    try {
        // finish
        copy.end();
        // which must fail
        std::cerr << "a row that is not an integer was accepted" << std::endl;
        return 1;
    }
    // with the condition the server named; SQLSTATE 22P02, invalid_text_representation
    catch (const DataError & error) {
        // check it
        if (error.diagnostic().sqlstate() != "22P02") {
            std::cerr << "the refusal came back as " << error.diagnostic().sqlstate() << std::endl;
            return 1;
        }
    }

    // the session is usable
    if (session.exec("SELECT 1").value(0, 0) != "1") {
        std::cerr << "the session is not usable after a refused copy" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
