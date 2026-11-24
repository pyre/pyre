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


// verify that asking the result of a statement that ran to raise its condition is a mistake of
// the caller, since there is no condition to raise
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // run a statement that succeeds
    const auto result = session.exec("SELECT 1");

    // attempt to
    try {
        // raise its condition
        result.raise("SELECT 1");
    }
    // the way the library reports a mistake of its caller
    catch (const InterfaceError & error) {
        // that names the statement
        if (error.diagnostic().command() != "SELECT 1") {
            std::cerr << "the refusal named '" << error.diagnostic().command() << "'" << std::endl;
            return 1;
        }
        // all done
        return 0;
    }
    // any other exception
    catch (const Exception & error) {
        std::cerr << "the result raised '" << error.what() << "'" << std::endl;
        return 1;
    }
}


// end of file
