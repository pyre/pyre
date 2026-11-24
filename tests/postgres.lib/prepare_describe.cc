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


// verify that the description of a prepared statement names the types of its parameters and of
// the columns of its rows
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // the identifier postgres catalogs its wide integers under
    constexpr oid_t int8 = 20;
    // and its narrow ones
    constexpr oid_t int4 = 23;

    // open a session
    const auto session = Connection(specification());
    // teach it a sum of two numbers of different widths
    session.prepare("pyre_sum", "SELECT $1::int8 + $2::int4 AS total");
    // and ask what it learned
    const auto description = session.describe("pyre_sum");

    // the statement takes two parameters
    if (description.parameters() != 2) {
        std::cerr << "the sum takes " << description.parameters() << " parameters" << std::endl;
        return 1;
    }
    // the first is wide
    if (description.parameterType(0) != int8) {
        std::cerr << "the first parameter is " << description.parameterType(0) << std::endl;
        return 1;
    }
    // the second is not
    if (description.parameterType(1) != int4) {
        std::cerr << "the second parameter is " << description.parameterType(1) << std::endl;
        return 1;
    }
    // its rows have one column
    if (description.columns() != 1) {
        std::cerr << "the sum has " << description.columns() << " columns" << std::endl;
        return 1;
    }
    // with the label it was given
    if (description.name(0) != "total") {
        std::cerr << "the column is labeled " << description.name(0) << std::endl;
        return 1;
    }
    // and the wider of the two types
    if (description.type(0) != int8) {
        std::cerr << "the column is of type " << description.type(0) << std::endl;
        return 1;
    }
    // and a description carries no rows
    if (description.rows() != 0) {
        std::cerr << "the description carried " << description.rows() << " rows" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
