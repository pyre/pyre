// -*- C++ -*-
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


// how many rows the scratch table holds
static auto
population(const pyre::postgres::Connection & session) -> long
{
    // ask the server
    return session.exec("SELECT count(*) FROM scratch")[0][0].as<long>();
}


// verify that a transaction opens as it is built, closes as it is destroyed, and that a statement
// which throws inside one does not leave it open behind it
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // and a table to scribble in, which goes away with the session
    session.exec("CREATE TEMP TABLE scratch (id int PRIMARY KEY)");

    // a transaction that is committed keeps what was done inside it
    {
        // open it
        auto work = Transaction(session);
        // which the server agrees is open
        if (session.transaction() != TransactionStatus::inTransaction) {
            std::cerr << "the server does not think a transaction is open" << std::endl;
            return 1;
        }
        // and so do we
        if (!work.live()) {
            std::cerr << "a freshly opened transaction is not live" << std::endl;
            return 1;
        }
        // do something
        session.execute("INSERT INTO scratch (id) VALUES ($1)", 1);
        // and keep it
        work.commit();
        // after which there is nothing left to close
        if (work.live()) {
            std::cerr << "a committed transaction is still live" << std::endl;
            return 1;
        }
    }
    // so the row is there
    if (population(session) != 1) {
        std::cerr << "a committed transaction did not keep its row" << std::endl;
        return 1;
    }
    // and the session is back where it started
    if (session.transaction() != TransactionStatus::idle) {
        std::cerr << "the session is still in a transaction after a commit" << std::endl;
        return 1;
    }

    // a transaction that is merely dropped undoes what was done inside it. this is the reason
    // the class exists: a caller that forgets to commit gets the safe answer, not a transaction
    // left open on the server until the session goes away
    {
        // open it
        auto work = Transaction(session);
        // do something
        session.execute("INSERT INTO scratch (id) VALUES ($1)", 2);
        // and walk away without saying anything
    }
    // so the row is not there
    if (population(session) != 1) {
        std::cerr << "an abandoned transaction kept its row" << std::endl;
        return 1;
    }

    // a transaction that is explicitly rolled back does the same
    {
        auto work = Transaction(session);
        session.execute("INSERT INTO scratch (id) VALUES ($1)", 3);
        work.rollback();
    }
    if (population(session) != 1) {
        std::cerr << "a rolled back transaction kept its row" << std::endl;
        return 1;
    }

    // and so does one whose scope is left by an exception, which is the case a caller cannot
    // write by hand without a great deal of care
    try {
        // open it
        auto work = Transaction(session);
        // do something that works
        session.execute("INSERT INTO scratch (id) VALUES ($1)", 4);
        // and then something that does not; this row is already there
        session.execute("INSERT INTO scratch (id) VALUES ($1)", 1);
        // so we never get here
        std::cerr << "a unique violation did not raise" << std::endl;
        return 1;
    }
    // the stack unwinds, the destructor runs, and the server hears about it
    catch (const IntegrityError &) {
        // as expected
    }
    // so neither row is there
    if (population(session) != 1) {
        std::cerr << "a transaction abandoned by an exception kept its row" << std::endl;
        return 1;
    }
    // and the session is usable again, rather than stuck refusing everything but a rollback
    if (session.transaction() != TransactionStatus::idle) {
        std::cerr << "the session is still in a transaction after an exception" << std::endl;
        return 1;
    }

    // closing a transaction twice is a mistake on this side of the wire
    {
        auto work = Transaction(session);
        work.rollback();
        try {
            work.commit();
            std::cerr << "committed a transaction that was already rolled back" << std::endl;
            return 1;
        }
        catch (const InterfaceError &) {
            // as expected
        }
    }

    // the duty to close a transaction may be handed on
    {
        // open one
        auto work = Transaction(session);
        // do something
        session.execute("INSERT INTO scratch (id) VALUES ($1)", 5);
        // and hand it to somebody else
        auto adopted = std::move(work);
        // who now owes the commit; the one it came from owes nothing
        if (work.live()) {
            std::cerr << "a transaction that was moved from is still live" << std::endl;
            return 1;
        }
        if (!adopted.live()) {
            std::cerr << "a transaction that was moved to is not live" << std::endl;
            return 1;
        }
        // and who pays it
        adopted.commit();
    }
    // so the row is there
    if (population(session) != 2) {
        std::cerr << "a transaction that was moved did not keep its row" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
