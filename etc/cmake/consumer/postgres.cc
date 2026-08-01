// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the postgres wrappers; this header reaches {libpq-fe.h}, so it compiles only if the
// libpq include directories arrive through the exported {pyre::postgres} target
#include <pyre/postgres.h>


// verify that the postgres add-on of an installation that carries it is reachable by a client
// that asks for the component and names nothing but {pyre::postgres}
// there is no connection attempt here on purpose: this checks the package, not the runtime, so
// it has to pass on a machine with no server of its own; the {pyre.db} and {pyre-postgres}
// suites are the ones that want a live database
int
main()
{
    // name a type from the wrappers; requiring it to be complete is what forces the compiler
    // to work through {libpq-fe.h}
    static_assert(sizeof(pyre::postgres::connection_t) > 0);

    // all done
    return 0;
}


// end of file
