// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>

// the package under test
#include <pyre/postgres.h>
// so a failing test can say why
#include <iostream>


// the session this suite runs on
static auto
specification() -> pyre::postgres::parameters_t
{
    // the one thing we insist on
    return pyre::postgres::parameters_t { { "dbname", "postgres" } };
}


// verify that the result of a statement that a pipeline skipped, because one ahead of it failed,
// raises an {OperationalError} that says the statement never ran, and names it
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // open a session
    const auto session = Connection(specification());
    // start a pipeline
    auto pipeline = Pipeline(session);
    // send a segment whose first statement fails
    pipeline.execute("SELECT 1/0", arguments_t {});
    pipeline.execute("SELECT 2", arguments_t {});
    pipeline.sync();

    // the first statement failed
    pipeline.next();
    // so the second was skipped
    const auto skipped = pipeline.next();
    if (!skipped || skipped->status() != ExecStatus::pipelineAborted) {
        std::cerr << "the statement after the failure was not skipped" << std::endl;
        return 1;
    }

    // attempt to
    try {
        // raise its condition
        skipped->raise("SELECT 2");
    }
    // the way the library reports a statement that the environment kept from running
    catch (const OperationalError & error) {
        // that names the statement
        if (error.diagnostic().command() != "SELECT 2") {
            std::cerr << "the failure named '" << error.diagnostic().command() << "'" << std::endl;
            return 1;
        }
        // and says what happened to it
        if (error.diagnostic().message().empty()) {
            std::cerr << "the failure did not say what happened" << std::endl;
            return 1;
        }
        // all done
        return 0;
    }
    // any other exception
    catch (const Exception & error) {
        std::cerr << "the result raised '" << error.what() << "'" << std::endl;
        return 1;
    }
}


// end of file
