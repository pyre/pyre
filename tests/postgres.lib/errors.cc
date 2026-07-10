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


// verify that the server's own name for what went wrong decides which exception is thrown
//
// this is the whole point of the exercise. the bindings this package replaces looked only at the
// message the server wrote for a human, and reported a unique index violation, a dropped
// connection and a typo in a table name as one and the same kind of failure
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());

    // a statement the parser cannot read; SQLSTATE 42601, syntax_error
    try {
        session.exec("SELECT FROM WHERE");
        std::cerr << "a syntax error did not raise" << std::endl;
        return 1;
    }
    catch (const ProgrammingError & error) {
        // the server named the condition
        if (error.diagnostic().sqlstate() != "42601") {
            std::cerr << "a syntax error came back as " << error.diagnostic().sqlstate()
                      << std::endl;
            return 1;
        }
        // and the report remembers what we asked it to run
        if (error.diagnostic().command() != "SELECT FROM WHERE") {
            std::cerr << "the diagnostic forgot the statement" << std::endl;
            return 1;
        }
        // and where in it the server gave up; postgres counts from one
        if (error.diagnostic().position() <= 0) {
            std::cerr << "the diagnostic does not say where the syntax error is" << std::endl;
            return 1;
        }
    }

    // a table that is not there; SQLSTATE 42P01, undefined_table
    try {
        session.exec("SELECT * FROM pyre_no_such_table");
        std::cerr << "an undefined table did not raise" << std::endl;
        return 1;
    }
    catch (const ProgrammingError & error) {
        if (error.diagnostic().sqlstate() != "42P01") {
            std::cerr << "an undefined table came back as " << error.diagnostic().sqlstate()
                      << std::endl;
            return 1;
        }
    }

    // a division that has no answer; SQLSTATE 22012, division_by_zero. this is a data exception,
    // and it must not be confused with a statement that was malformed: the statement is perfectly
    // well formed, and the data in it is not
    try {
        session.exec("SELECT 1/0");
        std::cerr << "a division by zero did not raise" << std::endl;
        return 1;
    }
    catch (const DataError & error) {
        if (error.diagnostic().sqlstate() != "22012") {
            std::cerr << "a division by zero came back as " << error.diagnostic().sqlstate()
                      << std::endl;
            return 1;
        }
    }

    // a value that is not what its type requires; SQLSTATE 22P02, invalid_text_representation
    try {
        session.exec("SELECT 'seven'::int");
        std::cerr << "a bad cast did not raise" << std::endl;
        return 1;
    }
    catch (const DataError & error) {
        if (error.diagnostic().sqlstate() != "22P02") {
            std::cerr << "a bad cast came back as " << error.diagnostic().sqlstate() << std::endl;
            return 1;
        }
    }

    // a statement that would leave the database inconsistent; SQLSTATE 23505, unique_violation.
    // this is the one that matters most to a caller, because it is the one that correct code
    // routinely expects: an insert that collides is how a program discovers a row is already there
    session.exec("CREATE TEMP TABLE unique_test (id int PRIMARY KEY)");
    session.exec("INSERT INTO unique_test (id) VALUES (1)");
    try {
        session.exec("INSERT INTO unique_test (id) VALUES (1)");
        std::cerr << "a unique violation did not raise" << std::endl;
        return 1;
    }
    catch (const IntegrityError & error) {
        if (error.diagnostic().sqlstate() != "23505") {
            std::cerr << "a unique violation came back as " << error.diagnostic().sqlstate()
                      << std::endl;
            return 1;
        }
        // and the server told us which constraint it was, so that a caller with two of them
        // need not read english to tell them apart
        if (error.diagnostic().constraint().empty()) {
            std::cerr << "the diagnostic does not name the constraint" << std::endl;
            return 1;
        }
        // nor which table it was on
        if (error.diagnostic().table() != "unique_test") {
            std::cerr << "the diagnostic does not name the table" << std::endl;
            return 1;
        }
    }

    // a foreign key that points at nothing; SQLSTATE 23503, foreign_key_violation, which is a
    // different condition in the same family, and hence the same exception
    session.exec("CREATE TEMP TABLE child (id int REFERENCES unique_test (id))");
    try {
        session.exec("INSERT INTO child (id) VALUES (99)");
        std::cerr << "a foreign key violation did not raise" << std::endl;
        return 1;
    }
    catch (const IntegrityError & error) {
        if (error.diagnostic().sqlstate() != "23503") {
            std::cerr << "a foreign key violation came back as " << error.diagnostic().sqlstate()
                      << std::endl;
            return 1;
        }
    }

    // every one of the above is a complaint from the server, so every one of them is catchable
    // as the base of that family
    try {
        session.exec("SELECT 1/0");
        std::cerr << "a division by zero did not raise" << std::endl;
        return 1;
    }
    catch (const DatabaseError &) {
        // as expected
    }

    // and as the base of everything the package throws
    try {
        session.exec("SELECT * FROM pyre_no_such_table");
        std::cerr << "an undefined table did not raise" << std::endl;
        return 1;
    }
    catch (const Exception & error) {
        // whose {what} is the one line summary, and which therefore says something
        if (string_t(error.what()).empty()) {
            std::cerr << "an exception has nothing to say for itself" << std::endl;
            return 1;
        }
    }

    // a mistake on this side of the wire is not a complaint from the server, and so is not a
    // {DatabaseError} at all
    try {
        session.exec("SELECT 1")[0]["neither"];
        std::cerr << "an unknown column did not raise" << std::endl;
        return 1;
    }
    catch (const DatabaseError &) {
        std::cerr << "an unknown column was blamed on the server" << std::endl;
        return 1;
    }
    catch (const InterfaceError & error) {
        // the server never saw this, so it has no name for it
        if (!error.diagnostic().sqlstate().empty()) {
            std::cerr << "an interface error carries a SQLSTATE" << std::endl;
            return 1;
        }
    }

    // a session survives every one of these; a failed statement outside a transaction leaves it
    // exactly where it was
    if (!session.ok() || session.transaction() != TransactionStatus::idle) {
        std::cerr << "the session did not survive the errors above" << std::endl;
        return 1;
    }
    // and still works
    if (session.exec("SELECT 1")[0][0].as<int>() != 1) {
        std::cerr << "the session cannot run a statement any more" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
