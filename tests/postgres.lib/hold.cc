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


// verify that a hold on a session holds it, with the session open, until it lets go, and that it
// sends statements through the session
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // take a hold on it
    auto held = session.hold("a hold");
    // which holds it
    if (!held.held() || !held.open()) {
        std::cerr << "the hold does not hold an open session" << std::endl;
        return 1;
    }
    // send a statement through it
    if (held.send("SELECT $1::integer", arguments_t { "42" }, false) == 0) {
        std::cerr << "the statement did not go out" << std::endl;
        return 1;
    }
    // collect its answer, through the session, whose lock the hold lets this thread take again
    const auto answer = session.result();
    // which holds the row
    if (!answer || answer->value(0, 0) != "42") {
        std::cerr << "the statement sent through the hold did not run" << std::endl;
        return 1;
    }
    // and nothing follows it
    if (session.result()) {
        std::cerr << "the session had more to say" << std::endl;
        return 1;
    }
    // let go
    held.release();
    // and the hold no longer holds the session
    if (held.held()) {
        std::cerr << "the hold still holds the session after letting go" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
