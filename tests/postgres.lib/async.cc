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
// and so it can hold the results it drains
#include <vector>


// the session this suite runs on
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// wait for the statement in flight to finish
//
// this is the loop the asynchronous calls exist to support: read whatever has arrived, ask
// whether the answer is complete, and go around again. the bindings this package replaces threw
// away the answer of {consume}, and so a loop like this one could not tell a socket that had
// gone quiet from one that had gone away
static auto
settle(const pyre::postgres::Connection & session) -> bool
{
    // a real client waits on the socket; a test may spin, as long as it gives up eventually
    for (long spins = 0; spins < 100000000L; ++spins) {
        // pull whatever the server has sent into libpq's buffer; a socket that has died raises
        session.consume();
        // and if the answer is complete
        if (!session.busy()) {
            // we are done waiting
            return true;
        }
    }

    // the server never answered
    return false;
}


// verify that a statement may be sent without waiting for it, that its results are collected one
// at a time, and that a failure among them does not derail the collection
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());

    // send a statement off without waiting for it
    session.send("SELECT 42");
    // wait for the server to finish with it
    if (!settle(session)) {
        std::cerr << "the server never answered" << std::endl;
        return 1;
    }

    // the first result is the answer
    const auto answer = session.result();
    // there is one
    if (!answer.has_value()) {
        std::cerr << "the statement produced no result" << std::endl;
        return 1;
    }
    // and it is what we asked for
    if (!answer->ok() || (*answer)[0][0].as<int>() != 42) {
        std::cerr << "the statement did not produce 42" << std::endl;
        return 1;
    }
    // the second is the sign that the server is done, and that the session may be used again
    if (session.result().has_value()) {
        std::cerr << "the statement produced a second result" << std::endl;
        return 1;
    }

    // the same, with the values kept out of the statement
    session.sendParams("SELECT $1::int * 2", arguments_t { "21" });
    if (!settle(session)) {
        std::cerr << "the server never answered the parameterized statement" << std::endl;
        return 1;
    }
    const auto doubled = session.result();
    if (!doubled.has_value() || (*doubled)[0][0].as<int>() != 42) {
        std::cerr << "the parameterized statement did not produce 42" << std::endl;
        return 1;
    }
    // drain it
    while (session.result().has_value()) {
    }

    // a statement that fails does not throw its way out of the collection loop. a session that
    // has sent a statement must collect every result the server produces for it before it may
    // send another, and a call that threw partway through would leave the session mid-answer
    session.send("SELECT * FROM pyre_no_such_table");
    if (!settle(session)) {
        std::cerr << "the server never answered the bad statement" << std::endl;
        return 1;
    }

    // so drain the whole answer, whatever it says
    std::vector<Result> harvest;
    while (const auto result = session.result()) {
        harvest.push_back(*result);
    }
    // the server produced exactly one result
    if (harvest.size() != 1) {
        std::cerr << "the bad statement produced " << harvest.size() << " results" << std::endl;
        return 1;
    }
    // which says the statement did not run
    if (harvest[0].ok()) {
        std::cerr << "a statement against a missing table reported success" << std::endl;
        return 1;
    }
    // and which, on request, names the condition the server named
    try {
        harvest[0].raise("SELECT * FROM pyre_no_such_table");
        std::cerr << "a failed result did not raise when asked" << std::endl;
        return 1;
    }
    catch (const ProgrammingError & error) {
        // the same classification the synchronous calls make
        if (error.diagnostic().sqlstate() != "42P01") {
            std::cerr << "the failed result was classified as " << error.diagnostic().sqlstate()
                      << std::endl;
            return 1;
        }
    }

    // and the session, having been drained, is usable again
    if (session.exec("SELECT 1")[0][0].as<int>() != 1) {
        std::cerr << "the session was left unusable" << std::endl;
        return 1;
    }

    // a message from another session; there is only one session here, and postgres is happy to
    // deliver a notification to the session that raised it
    session.exec("LISTEN pyre_channel");
    session.exec("NOTIFY pyre_channel, 'the payload'");
    // notifications ride on the back of ordinary traffic, so they must be read off the socket
    session.consume();

    // collect the one we sent
    const auto message = session.notification();
    // there is one
    if (!message.has_value()) {
        std::cerr << "the notification never arrived" << std::endl;
        return 1;
    }
    // on the channel we named
    if (message->channel != "pyre_channel") {
        std::cerr << "the notification arrived on channel '" << message->channel << "'"
                  << std::endl;
        return 1;
    }
    // carrying what we sent
    if (message->payload != "the payload") {
        std::cerr << "the notification carried '" << message->payload << "'" << std::endl;
        return 1;
    }
    // from this very session
    if (message->backend != session.backend()) {
        std::cerr << "the notification came from another back end" << std::endl;
        return 1;
    }
    // and there are no more
    if (session.notification().has_value()) {
        std::cerr << "a second notification arrived" << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
