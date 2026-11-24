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


// verify that a copy out of the database abandoned inside a transaction leaves the transaction
// able to go on and keep its work
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec("CREATE TEMPORARY TABLE pyre_copy (id integer)");
    // start a transaction
    session.exec("BEGIN");
    // that does some work
    session.exec("INSERT INTO pyre_copy (id) VALUES (1)");

    // in a scope of its own
    {
        // start a copy of many rows
        auto copy = CopyOut(session, "COPY (SELECT generate_series(1, 100000)) TO STDOUT");
        // take the first
        const auto line = copy.next();
        // which is there
        if (!line || *line != "1\n") {
            std::cerr << "the first row did not come out" << std::endl;
            return 1;
        }
        // and leave without the others
    }

    // the transaction is still good
    if (session.transaction() != TransactionStatus::inTransaction) {
        std::cerr << "the abandoned copy failed the transaction" << std::endl;
        return 1;
    }
    // so it can go on
    session.exec("INSERT INTO pyre_copy (id) VALUES (2)");
    // and keep its work
    if (session.exec("COMMIT").command() != "COMMIT") {
        std::cerr << "the transaction did not commit" << std::endl;
        return 1;
    }
    // all of it
    if (session.exec("SELECT count(*) FROM pyre_copy").value(0, 0) != "2") {
        std::cerr << "the transaction lost its work" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
