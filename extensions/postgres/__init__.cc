// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the module entry point
//
// note that nothing here reaches back into {pyre.db} as the module is imported. the package
// imports the component that imports us, so an import in the other direction would close the
// cycle; the one thing that needs it, the exception hierarchy, waits until it is asked
PYBIND11_MODULE(postgres, m)
{
    // the docstring
    m.doc() = "provides access to PostgreSQL databases, over libpq";

    // the exception hierarchy, first, so that everything registered below it can raise
    pyre::postgres::py::exceptions(m);
    // the enumerations, next, since the properties below hand back their values
    pyre::postgres::py::enums(m);

    // what the server says when a statement does not work out
    pyre::postgres::py::diagnostic(m);

    // what it sends back when one does; the result hands back rows, and the rows hand back
    // fields, so they must all be registered before anybody calls one of their methods
    pyre::postgres::py::field(m);
    pyre::postgres::py::row(m);
    pyre::postgres::py::result(m);

    // what other sessions have to say
    pyre::postgres::py::notification(m);

    // the session, which hands back results and notifications
    pyre::postgres::py::connection(m);
    // and the scope of the work done over it, which is built out of a session
    pyre::postgres::py::transaction(m);

    // the loose functions, last
    pyre::postgres::py::utilities(m);

    // all done
    return;
}


// end of file
