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


// verify that a copy out of the database hands back each row as a line of text, and nothing
// once they are all out
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());

    // start a copy of two rows
    auto copy = CopyOut(session, "COPY (VALUES (1, 'one'), (2, 'two')) TO STDOUT");
    // collect what comes out
    std::vector<string_t> lines;
    // one row at a time
    while (auto line = copy.next()) {
        // keep it
        lines.push_back(*line);
    }

    // the rows came out as lines of text
    if (lines != std::vector<string_t> { "1\tone\n", "2\ttwo\n" }) {
        std::cerr << "the copy handed back " << lines.size() << " other lines" << std::endl;
        return 1;
    }
    // and the copy is over
    if (copy.live()) {
        std::cerr << "a copy that handed back all its rows is still live" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
