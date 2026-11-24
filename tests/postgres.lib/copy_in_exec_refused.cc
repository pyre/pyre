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


// verify that a statement sent through a session in the middle of a copy into the database is
// refused as a misuse of the interface, and that the copy keeps every row it is sent
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
    auto copy = CopyIn(session, "COPY pyre_copy (id) FROM STDIN");
    // send a row
    copy.record(1);

    // attempt to
    try {
        // send another statement in the middle of the copy
        session.exec("SELECT 42");
        // which must fail
        std::cerr << "a statement sent in the middle of a copy was accepted" << std::endl;
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

    // send another row
    copy.record(2);
    // and finish
    const auto result = copy.end();
    // the server kept both
    if (result.affected() != 2) {
        std::cerr << "the copy reported " << result.affected() << " rows" << std::endl;
        return 1;
    }

    // and the table holds them
    if (session.exec("SELECT count(*) FROM pyre_copy").value(0, 0) != "2") {
        std::cerr << "the table does not hold the rows of the copy" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
