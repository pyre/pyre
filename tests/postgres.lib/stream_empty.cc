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


// verify that a stream over a selection with no rows hands back no batches, and leaves the
// session free
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // stream a selection with no rows
    auto stream = Stream(session, "SELECT 1 WHERE false", arguments_t(), 2);

    // there is no batch
    if (stream.next()) {
        std::cerr << "a selection with no rows handed back a batch" << std::endl;
        return 1;
    }
    // and the session is free
    if (session.transaction() != TransactionStatus::idle) {
        std::cerr << "the session is not free after the stream" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
