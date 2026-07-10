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


// verify that the values of a c++ program survive the trip to the server and back, and that a
// value sent as an argument stays a value: it never becomes part of the statement that carries it
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());

    // whole numbers, at both ends of their range
    if (session.execute("SELECT $1::int", 42)[0][0].as<int>() != 42) {
        std::cerr << "an int did not survive the round trip" << std::endl;
        return 1;
    }
    if (session.execute("SELECT $1::int", -7)[0][0].as<int>() != -7) {
        std::cerr << "a negative int did not survive the round trip" << std::endl;
        return 1;
    }
    // the widest whole number postgres has; the text of this one is nineteen digits long, and a
    // client that read it into an {int} would lose almost all of it
    const std::int64_t big = 9223372036854775807LL;
    if (session.execute("SELECT $1::bigint", big)[0][0].as<std::int64_t>() != big) {
        std::cerr << "a bigint did not survive the round trip" << std::endl;
        return 1;
    }

    // a whole number that will not fit is a data exception, not a silently truncated answer
    try {
        // this is the widest {bigint}, and it does not fit in an {int}
        session.execute("SELECT $1::bigint", big)[0][0].as<std::int32_t>();
        std::cerr << "a bigint fit into an int" << std::endl;
        return 1;
    }
    catch (const DataError &) {
        // as expected
    }
    // and neither does text that is not a number at all
    try {
        session.exec("SELECT 'seven'")[0][0].as<int>();
        std::cerr << "the word 'seven' parsed as a number" << std::endl;
        return 1;
    }
    catch (const DataError &) {
        // as expected
    }

    // real numbers, which are the ones a naive rendering loses. one third has no exact decimal
    // expansion, so a client that wrote it with the six digits {std::to_string} produces would
    // get a different number back than the one it sent
    const double third = 1.0 / 3.0;
    if (session.execute("SELECT $1::float8", third)[0][0].as<double>() != third) {
        std::cerr << "a double did not survive the round trip" << std::endl;
        return 1;
    }
    // and the three values whose spelling postgres does not share with c++
    const auto infinite = session.execute("SELECT $1::float8", HUGE_VAL)[0][0].as<double>();
    if (!std::isinf(infinite) || infinite < 0) {
        std::cerr << "positive infinity did not survive the round trip" << std::endl;
        return 1;
    }
    const auto nan = session.execute("SELECT $1::float8", std::nan(""))[0][0].as<double>();
    if (!std::isnan(nan)) {
        std::cerr << "a NaN did not survive the round trip" << std::endl;
        return 1;
    }

    // truth, which postgres writes as a single letter
    if (session.execute("SELECT $1::bool", true)[0][0].as<bool>() != true) {
        std::cerr << "true did not survive the round trip" << std::endl;
        return 1;
    }
    if (session.execute("SELECT $1::bool", false)[0][0].as<bool>() != false) {
        std::cerr << "false did not survive the round trip" << std::endl;
        return 1;
    }

    // text, including a string literal, which decays to a pointer and must still find its recipe
    if (session.execute("SELECT $1::text", "hello")[0][0].as<string_t>() != "hello") {
        std::cerr << "a string literal did not survive the round trip" << std::endl;
        return 1;
    }
    // and text with a zero length, which is not a NULL
    const auto blank = session.execute("SELECT $1::text", string_t(""))[0][0];
    if (blank.isNull() || !blank.as<string_t>().empty()) {
        std::cerr << "the empty string came back as a NULL" << std::endl;
        return 1;
    }

    // this is the reason the arguments travel beside the statement rather than inside it. the
    // text below closes a quote, ends the statement, drops a table and comments out whatever
    // followed; spliced into sql it would do all of that, and here it is just a value
    const string_t mischief = "'); DROP TABLE pg_class; --";
    const auto echoed = session.execute("SELECT $1::text", mischief)[0][0].as<string_t>();
    // it comes back exactly as it went
    if (echoed != mischief) {
        std::cerr << "a value with sql in it did not come back intact" << std::endl;
        return 1;
    }
    // and the catalog it named is still there
    if (session.exec("SELECT count(*) FROM pg_class")[0][0].as<long>() <= 0) {
        std::cerr << "the argument was executed rather than bound" << std::endl;
        return 1;
    }

    // an absent value; this is how a caller spells {NULL}, and there is no other way
    const auto nothing = session.execute("SELECT $1::int", std::optional<int>())[0][0];
    if (!nothing.isNull()) {
        std::cerr << "an empty optional did not become a NULL" << std::endl;
        return 1;
    }
    // while one that holds something is that something
    const auto something = session.execute("SELECT $1::int", std::optional<int>(5))[0][0];
    if (something.isNull() || something.as<int>() != 5) {
        std::cerr << "a full optional did not become its value" << std::endl;
        return 1;
    }

    // raw octets, including the zero that no text may hold
    const bytes_t octets { std::byte { 0x00 }, std::byte { 0xff }, std::byte { 0x10 },
                           std::byte { 'a' } };
    const auto returned = session.execute("SELECT $1::bytea", octets)[0][0].as<bytes_t>();
    // which come back one for one
    if (returned != octets) {
        std::cerr << "a byte string did not survive the round trip" << std::endl;
        return 1;
    }

    // several arguments at once, of unlike types
    const auto sum = session.execute("SELECT $1::int + $2::int", 20, 22)[0][0].as<int>();
    if (sum != 42) {
        std::cerr << "two arguments did not add up" << std::endl;
        return 1;
    }
    // and none at all, which still goes through the extended protocol
    if (session.execute("SELECT 1")[0][0].as<int>() != 1) {
        std::cerr << "a statement with no arguments did not run" << std::endl;
        return 1;
    }

    // a statement the server has been taught, run twice with different arguments
    session.prepare("doubler", "SELECT $1::int * 2");
    if (session.execPrepared("doubler", arguments_t { "21" })[0][0].as<int>() != 42) {
        std::cerr << "a prepared statement did not run" << std::endl;
        return 1;
    }
    if (session.execPrepared("doubler", arguments_t { "50" })[0][0].as<int>() != 100) {
        std::cerr << "a prepared statement did not run a second time" << std::endl;
        return 1;
    }
    // and an argument that is absent, spelled the way {arguments_t} spells it
    const auto none = session.execPrepared("doubler", arguments_t { argument_t() })[0][0];
    if (!none.isNull()) {
        std::cerr << "an absent argument to a prepared statement was not a NULL" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
