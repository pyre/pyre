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
// the sizes of the batches
#include <vector>


// the session this suite runs on
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// verify that a stream hands back the rows of a selection in batches of the size it was asked
// for, as libpq delivers them, and leaves the session free once they are all read
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // stream five rows, two at a time
    auto stream = Stream(session, "SELECT generate_series(1, 5)", arguments_t(), 2);

    // the sizes of the batches
    std::vector<int> sizes;
    // and the values of the rows, in order
    string_t values;
    // go through the batches
    while (const auto batch = stream.next()) {
        // record the size of each
        sizes.push_back(batch->rows());
        // and the values of its rows
        for (auto row = 0; row < batch->rows(); ++row) {
            // one at a time
            values += string_t(batch->value(row, 0)) + " ";
        }
    }

    // every row arrived, in order
    if (values != "1 2 3 4 5 ") {
        std::cerr << "the stream handed back " << values << std::endl;
        return 1;
    }

    // the rows arrive in chunks, each batch full but the last
    const std::vector<int> expected { 2, 2, 1 };
    // check
    if (sizes != expected) {
        std::cerr << "the stream handed back " << sizes.size() << " batches of other sizes"
                  << std::endl;
        return 1;
    }

    // the stream is over
    if (stream.live()) {
        std::cerr << "the stream is live after its last row" << std::endl;
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
