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


// verify that a stream whose statement fails partway hands back the rows made before the failure,
// reports the failure as the condition the server named, and leaves the session usable
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // stream a selection that divides by zero at its third row, one row at a time
    auto stream =
        Stream(session, "SELECT 10 / (3 - n) FROM generate_series(1, 5) AS n", arguments_t(), 1);

    // the values of the rows that arrive
    string_t values;
    // attempt to
    try {
        // go through the batches
        while (const auto batch = stream.next()) {
            // and the rows of each
            for (auto row = 0; row < batch->rows(); ++row) {
                // record the value
                values += string_t(batch->value(row, 0)) + " ";
            }
        }
        // the stream must fail
        std::cerr << "a stream that divides by zero ended without a word" << std::endl;
        return 1;
    }
    // as the condition the server named
    catch (const DataError & error) {
        // division by zero
        if (error.diagnostic().sqlstate() != "22012") {
            std::cerr << "the stream failed with " << error.diagnostic().sqlstate() << std::endl;
            return 1;
        }
    }

    // the rows before the failure arrived
    if (values != "5 10 ") {
        std::cerr << "the stream handed back " << values << std::endl;
        return 1;
    }
    // the stream is over
    if (stream.live()) {
        std::cerr << "the stream is live after its failure" << std::endl;
        return 1;
    }
    // and the session is usable
    if (session.exec("SELECT 1").value(0, 0) != "1") {
        std::cerr << "the session is not usable after a failed stream" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
