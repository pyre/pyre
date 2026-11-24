// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>

// the package under test
#include <pyre/postgres.h>
// so a failing test can say why
#include <iostream>


// the session this suite runs on
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// verify that rolling back a transaction opened inside another undoes only its own work
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // and a scratch table, which goes away with the session
    session.exec("CREATE TEMP TABLE scratch (id int)");

    // open a transaction
    auto outer = Transaction(session);
    // do something in it
    session.exec("INSERT INTO scratch (id) VALUES (1)");
    // open another inside it
    auto inner = Transaction(session);
    // do something in that one
    session.exec("INSERT INTO scratch (id) VALUES (2)");
    // and undo it
    inner.rollback();
    // the outer transaction is still open, so commit it
    outer.commit();

    // the work of the outer transaction was kept, and that of the inner one undone
    const auto rows = session.exec("SELECT count(*) FROM scratch")[0][0].as<long>();
    // so check
    if (rows != 1) {
        // and complain if not
        std::cerr << rows << " rows survived instead of 1" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
