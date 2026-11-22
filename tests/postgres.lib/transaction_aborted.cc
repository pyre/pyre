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


// verify that committing a transaction the server has abandoned says that nothing was kept
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
    auto work = Transaction(session);
    // do something in it
    session.exec("INSERT INTO scratch (id) VALUES (1)");
    // make a statement fail, which makes the server abandon the transaction
    try {
        // by dividing by zero
        session.exec("SELECT 1/0");
        // so we never get here
        std::cerr << "a division by zero did not raise" << std::endl;
        return 1;
    }
    // swallow the error, as careless code might
    catch (const DataError &) {
        // and go on
    }

    // the commit cannot keep anything
    try {
        // so try it
        work.commit();
        // and complain if it says otherwise
        std::cerr << "the commit of an abandoned transaction reported success" << std::endl;
        return 1;
    }
    // it must say so
    catch (const OperationalError &) {
        // as expected
    }

    // either way, the work is not there
    const auto rows = session.exec("SELECT count(*) FROM scratch")[0][0].as<long>();
    // so check
    if (rows != 0) {
        // and complain if it is
        std::cerr << "the work of an abandoned transaction was kept" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
