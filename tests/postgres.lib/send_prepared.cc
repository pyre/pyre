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


// collect the answer to the statement in flight: the one result it makes, and the end after it
static auto
collect(const pyre::postgres::Connection & session) -> std::optional<pyre::postgres::Result>
{
    // the result
    const auto answer = session.result();
    // and the end of the answer, which must follow it
    if (session.result()) {
        // or the session had more to say
        return std::nullopt;
    }
    // hand it over
    return answer;
}


// verify that a statement can be prepared and run without waiting for the server, and that its
// answers are collected as those of any statement sent off
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());

    // teach the server a statement, without waiting
    session.sendPrepare("pyre_send_prepared", "SELECT $1::integer * 2");
    // collect the answer
    const auto prepared = collect(session);
    // which says the statement was taught
    if (!prepared || !prepared->ok()) {
        std::cerr << "the statement was not prepared" << std::endl;
        return 1;
    }

    // run it, without waiting
    session.sendPrepared("pyre_send_prepared", arguments_t { "21" });
    // collect the answer
    const auto answer = collect(session);
    // which holds the row
    if (!answer || answer->rows() != 1 || answer->value(0, 0) != "42") {
        std::cerr << "the prepared statement did not run" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
