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


// verify what releasing a statement does inside a transaction that has failed: a libpq that can
// close a prepared statement does so even there, and an older one, which has to ask the server to
// {DEALLOCATE} it, is refused until the transaction ends
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // teach it a statement
    session.prepare("pyre_one", "SELECT 1");

    // start a transaction
    session.exec("BEGIN");
    // attempt to
    try {
        // run a statement that fails
        session.exec("SELECT 1/0");
        // which must fail
        std::cerr << "the division by zero ran" << std::endl;
        return 1;
    }
    // the way the server reports a bad value, which leaves the transaction failed
    catch (const DataError & error) {
        // make sure it is the division that failed
        if (error.diagnostic().sqlstate() != "22012") {
            std::cerr << "the division failed with " << error.diagnostic().sqlstate() << std::endl;
            return 1;
        }
    }

#if defined(LIBPQ_HAS_CLOSE_PREPARED)
    // release the statement; this one closes it even in a failed transaction
    session.release("pyre_one");
    // end the transaction
    session.exec("ROLLBACK");
    // attempt to
    try {
        // run what was released
        session.execPrepared("pyre_one", {});
        // which must fail
        std::cerr << "a statement released in a failed transaction ran" << std::endl;
        return 1;
    }
    // the way the server reports a missing prepared statement
    catch (const OperationalError & error) {
        // with its own code for it
        if (error.diagnostic().sqlstate() != "26000") {
            std::cerr << "the refusal carried " << error.diagnostic().sqlstate() << std::endl;
            return 1;
        }
    }
#else
    // attempt to
    try {
        // release the statement, which this libpq does with a {DEALLOCATE}
        session.release("pyre_one");
        // which must fail in a failed transaction
        std::cerr << "a statement was deallocated in a failed transaction" << std::endl;
        return 1;
    }
    // the way the server reports a statement sent to a failed transaction
    catch (const InternalError & error) {
        // with its own code for it
        if (error.diagnostic().sqlstate() != "25P02") {
            std::cerr << "the refusal carried " << error.diagnostic().sqlstate() << std::endl;
            return 1;
        }
    }
    // end the transaction
    session.exec("ROLLBACK");
    // and the statement is still there
    if (session.execPrepared("pyre_one", {}).value(0, 0) != "1") {
        std::cerr << "the refused release removed the statement" << std::endl;
        return 1;
    }
#endif

    // all done
    return 0;
}


// end of file
