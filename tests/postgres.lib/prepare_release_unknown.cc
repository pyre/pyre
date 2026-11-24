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


// verify what releasing a name the session was never taught does: a libpq that can close a
// prepared statement finds nothing to close, which the protocol does not count as an error, and an
// older one, which has to ask the server to {DEALLOCATE} it, is refused
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());

#if defined(LIBPQ_HAS_CLOSE_PREPARED)
    // release a statement nobody prepared, which is not a mistake
    session.release("pyre_nothing");
    // and the session is usable
    if (session.exec("SELECT 1").value(0, 0) != "1") {
        std::cerr << "the session is not usable after releasing nothing" << std::endl;
        return 1;
    }
#else
    // attempt to
    try {
        // release a statement nobody prepared
        session.release("pyre_nothing");
        // which must fail
        std::cerr << "a name nobody prepared was deallocated" << std::endl;
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
#endif

    // all done
    return 0;
}


// end of file
