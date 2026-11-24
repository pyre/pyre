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


// verify that committing a transaction opened inside another leaves the outer one open, so that
// undoing the outer one undoes both
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
    // open another inside it
    auto inner = Transaction(session);
    // do something in the inner one
    session.exec("INSERT INTO scratch (id) VALUES (1)");
    // and commit it
    inner.commit();
    // the outer one must still be open
    if (session.transaction() != TransactionStatus::inTransaction) {
        // so complain if the inner commit closed it
        std::cerr << "the commit of an inner transaction closed the outer one" << std::endl;
        return 1;
    }
    // undo the outer one
    outer.rollback();

    // nothing survives
    const auto rows = session.exec("SELECT count(*) FROM scratch")[0][0].as<long>();
    // so check
    if (rows != 0) {
        // and complain if something did
        std::cerr << rows << " rows survived instead of none" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
