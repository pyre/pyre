// -*- C++ -*-
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


// verify that a statement runs, that its result reports its own shape, and that the rows and
// fields taken out of it read what the server sent
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());

    // run something with a shape we know
    const auto result = session.exec("SELECT 1 AS one, 'two' AS two");
    // the server ran it
    if (!result.ok()) {
        std::cerr << "the statement did not run" << std::endl;
        return 1;
    }
    // and it returned rows
    if (result.status() != ExecStatus::tuplesOk) {
        std::cerr << "a select did not report rows" << std::endl;
        return 1;
    }
    // one of them
    if (result.rows() != 1) {
        std::cerr << "expected one row, got " << result.rows() << std::endl;
        return 1;
    }
    // holding two values
    if (result.columns() != 2) {
        std::cerr << "expected two columns, got " << result.columns() << std::endl;
        return 1;
    }
    // under the names we gave them
    if (result.name(0) != "one" || result.name(1) != "two") {
        std::cerr << "the columns came back under the wrong names" << std::endl;
        return 1;
    }
    // which we can look up
    if (result.column("two") != 1) {
        std::cerr << "could not find the column named 'two'" << std::endl;
        return 1;
    }
    // and a name that is not there answers, rather than raising; this is the one query in the
    // package that does
    if (result.column("neither") != unknownColumn) {
        std::cerr << "found a column that is not there" << std::endl;
        return 1;
    }
    // the values are the text the server's output functions produced
    if (result.value(0, 0) != "1" || result.value(0, 1) != "two") {
        std::cerr << "the values are not what the server sent" << std::endl;
        return 1;
    }

    // the same, through a row
    const auto row = result[0];
    // which holds as many values as the result has columns
    if (row.size() != 2) {
        std::cerr << "the row does not have two fields" << std::endl;
        return 1;
    }
    // reachable by position
    if (row[0].as<int>() != 1) {
        std::cerr << "the first field is not the number one" << std::endl;
        return 1;
    }
    // and by name
    if (row["two"].as<string_t>() != "two") {
        std::cerr << "the field named 'two' does not hold 'two'" << std::endl;
        return 1;
    }
    // each of which knows where it came from
    if (row[0].name() != "one" || row[0].type() == invalidOid) {
        std::cerr << "a field does not know its own column" << std::endl;
        return 1;
    }

    // a subscript past the end of a result is a mistake on this side of the wire
    try {
        // there is no second row
        result[1];
        // so getting here is a failure
        std::cerr << "read a row that is not there" << std::endl;
        return 1;
    }
    // and this is how we hear about it, rather than by libpq writing on stderr and handing back
    // a null pointer for us to dereference
    catch (const InterfaceError &) {
        // as expected
    }

    // as is a column that the result does not carry
    try {
        // there is no such name
        row["neither"];
        // so getting here is a failure
        std::cerr << "read a column that is not there" << std::endl;
        return 1;
    }
    catch (const InterfaceError &) {
        // as expected
    }

    // a result may be walked
    const auto series = session.exec("SELECT n FROM generate_series(1, 5) AS n");
    // and it should have five rows
    if (series.rows() != 5) {
        std::cerr << "expected five rows, got " << series.rows() << std::endl;
        return 1;
    }
    // add them up, one row at a time
    int total = 0;
    for (const auto & entry : series) {
        // each row holds exactly one field, which we may also walk
        for (const auto & field : entry) {
            total += field.as<int>();
        }
    }
    // and the first five whole numbers add up to fifteen
    if (total != 15) {
        std::cerr << "the rows add up to " << total << ", not 15" << std::endl;
        return 1;
    }

    // a field the server did not send is not the empty string, and the difference is one that
    // c++ has no way to spell without help
    const auto absent = session.exec("SELECT NULL::int AS nothing");
    // so the field says so
    if (!absent[0][0].isNull()) {
        std::cerr << "a NULL did not report itself as one" << std::endl;
        return 1;
    }
    // and it is false in a boolean context, whatever it might have held
    if (absent[0][0]) {
        std::cerr << "a NULL is true in a boolean context" << std::endl;
        return 1;
    }
    // asking it for a number is an error, because there is no number to hand back
    try {
        absent[0][0].as<int>();
        std::cerr << "read a number out of a NULL" << std::endl;
        return 1;
    }
    // and a value that is not what its type requires is a data exception
    catch (const DataError &) {
        // as expected
    }
    // a caller that expected this asks for an optional
    if (absent[0][0].optional<int>().has_value()) {
        std::cerr << "a NULL produced an optional that holds something" << std::endl;
        return 1;
    }
    // or supplies something to use in its place
    if (absent[0][0].as<int>(-1) != -1) {
        std::cerr << "a NULL did not fall back on the value we gave it" << std::endl;
        return 1;
    }

    // {exec} runs several statements at once, and reports on the last of them
    const auto several = session.exec("SELECT 1; SELECT 2");
    // so this holds the second
    if (several[0][0].as<int>() != 2) {
        std::cerr << "a multi statement command did not report on its last statement" << std::endl;
        return 1;
    }

    // a statement that changes something reports how much
    session.exec("CREATE TEMP TABLE counted (id int)");
    const auto inserted = session.exec("INSERT INTO counted (id) VALUES (1), (2), (3)");
    // it returned no rows
    if (inserted.status() != ExecStatus::commandOk) {
        std::cerr << "an insert reported rows" << std::endl;
        return 1;
    }
    // but it touched three of them
    if (inserted.affected() != 3) {
        std::cerr << "the insert touched " << inserted.affected() << " rows, not 3" << std::endl;
        return 1;
    }
    // and the server tagged it as what it was
    if (inserted.command().substr(0, 6) != "INSERT") {
        std::cerr << "the insert came back tagged '" << inserted.command() << "'" << std::endl;
        return 1;
    }

    // a statement that is nothing but whitespace is a statement that ran, trivially
    const auto empty = session.exec("");
    // and says so
    if (empty.status() != ExecStatus::emptyQuery || !empty.ok()) {
        std::cerr << "an empty statement was not recognized as one" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
