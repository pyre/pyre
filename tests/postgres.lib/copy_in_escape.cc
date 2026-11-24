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


// verify that text holding the characters that mean something to the format of a copy, a tab, a
// newline and a backslash, arrives as it was sent, and that a missing value arrives as {NULL}
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // make a table of our own, which goes away with the session
    session.exec(
        "CREATE TEMPORARY TABLE pyre_copy (tab text, newline text, slash text, nothing text)");

    // start a copy into it
    auto copy = CopyIn(session, "COPY pyre_copy FROM STDIN");
    // send a row of awkward text
    copy.record(string_t("a\tb"), string_t("c\nd"), string_t("e\\f"), std::optional<string_t>());
    // and finish
    copy.end();

    // read it back
    const auto rows = session.exec("SELECT tab, newline, slash, nothing FROM pyre_copy");
    // the text arrived as it was sent
    if (rows.value(0, 0) != "a\tb" || rows.value(0, 1) != "c\nd" || rows.value(0, 2) != "e\\f") {
        std::cerr << "the text came back changed" << std::endl;
        return 1;
    }
    // and the missing value is {NULL}
    if (!rows.isNull(0, 3)) {
        std::cerr << "a missing value came back as " << rows.value(0, 3) << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
