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


// the session this suite runs on; libpq fills in the host, the port and the role from the
// environment, exactly as {psql} does
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// verify that a session comes up, reports on itself, and goes down; and that a session that has
// gone down stays down, however many copies of it are still lying around
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    auto session = Connection(specification());
    // it should be up
    if (!session.ok()) {
        std::cerr << "the session did not come up: " << session.message() << std::endl;
        return 1;
    }
    // and talking to the database we asked for
    if (session.database() != "postgres") {
        std::cerr << "connected to '" << session.database() << "', not 'postgres'" << std::endl;
        return 1;
    }
    // to a server that told us its version
    if (session.server() <= 0) {
        std::cerr << "the server did not report its version" << std::endl;
        return 1;
    }
    // over a socket
    if (session.socket() < 0) {
        std::cerr << "the session has no socket" << std::endl;
        return 1;
    }
    // with a back end behind it
    if (session.backend() <= 0) {
        std::cerr << "the session has no back end" << std::endl;
        return 1;
    }
    // and with no transaction open
    if (session.transaction() != TransactionStatus::idle) {
        std::cerr << "a freshly opened session is already in a transaction" << std::endl;
        return 1;
    }

    // take a copy of it; the two now share one session with the server
    auto alias = session;
    // which the copy can use
    const auto result = alias.exec("SELECT 1");
    // and which answers
    if (result.rows() != 1) {
        std::cerr << "the copy could not run a statement" << std::endl;
        return 1;
    }

    // now close the session through one of them
    session.close();

    // the one that closed it knows
    if (session.ok()) {
        std::cerr << "a closed session still reports itself as up" << std::endl;
        return 1;
    }
    // and so does the copy, which is the whole point of boxing the pointer: the bindings this
    // package replaces would have handed libpq an address it had already freed
    if (alias.ok()) {
        std::cerr << "a copy of a closed session still reports itself as up" << std::endl;
        return 1;
    }

    // a statement sent through the copy is a mistake on this side of the wire
    try {
        // so this must not reach the server, and must not touch the freed session
        alias.exec("SELECT 1");
        // getting here means it did
        std::cerr << "a copy of a closed session ran a statement" << std::endl;
        return 1;
    }
    // and this is how we hear about it
    catch (const InterfaceError &) {
        // as expected
    }

    // closing a session twice is harmless
    session.close();
    // and so is closing it through the copy
    alias.close();

    // a session that cannot be established raises, rather than handing back something unusable
    try {
        // there is no database by this name, and there had better not be
        auto missing = Connection(parameters_t { { "dbname", "pyre-no-such-database" } });
        // so getting here means the server let us in
        std::cerr << "connected to a database that does not exist" << std::endl;
        return 1;
    }
    // a connection that will not come up is environmental, always
    catch (const OperationalError & error) {
        // and libpq should have said something about it
        if (error.diagnostic().message().empty()) {
            std::cerr << "a failed connection came with no explanation" << std::endl;
            return 1;
        }
    }

    // all done
    return 0;
}


// end of file
