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


// verify that the result of a copy sent with the asynchronous calls is refused as a misuse of the
// interface, rather than handed back over and over, and that the session is usable afterwards
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec("CREATE TEMPORARY TABLE pyre_copy (id integer)");

    // send the copy without waiting for it
    session.send("COPY pyre_copy FROM STDIN");
    // attempt to
    try {
        // collect its result
        session.result();
        // which must fail
        std::cerr << "the result of a copy was handed back" << std::endl;
        return 1;
    }
    // as a misuse of the interface
    catch (const InterfaceError & error) {
        // that names the calls a copy runs through
        if (string_t(error.what()).find("copyIn") == string_t::npos) {
            std::cerr << "the refusal said: " << error.what() << std::endl;
            return 1;
        }
    }

    // the answer has been collected
    if (session.result()) {
        std::cerr << "the copy left results behind" << std::endl;
        return 1;
    }
    // and the session is usable
    if (session.exec("SELECT 1").value(0, 0) != "1") {
        std::cerr << "the session is not usable after a refused copy" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
