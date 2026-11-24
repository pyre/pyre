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


// verify that a stream fills the placeholders of its statement from its arguments
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // stream the rows of a series whose bounds travel beside the statement
    auto stream = Stream(
        session, "SELECT generate_series($1::integer, $2::integer)", arguments_t { "3", "7" }, 10);

    // the values of the rows, in order
    string_t values;
    // go through the batches
    while (const auto batch = stream.next()) {
        // and the rows of each
        for (auto row = 0; row < batch->rows(); ++row) {
            // record the value
            values += string_t(batch->value(row, 0)) + " ";
        }
    }

    // the rows are the ones the arguments asked for
    if (values != "3 4 5 6 7 ") {
        std::cerr << "the stream handed back " << values << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
