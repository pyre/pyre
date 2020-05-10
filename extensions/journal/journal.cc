// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the module entry point
PYBIND11_MODULE(journal, m) {
    // the doc string
    m.doc() = "the journal extension module";

    // bind the opaque types
    pyre::libjournal::opaque(m);
    // register the exception types
    pyre::libjournal::exceptions(m);

    // global state
    pyre::libjournal::chronicler(m);
    // devices
    pyre::libjournal::devices(m);
    // developer channels
    pyre::libjournal::debug(m);
    pyre::libjournal::firewall(m);
    // user facing channels
    pyre::libjournal::info(m);
    pyre::libjournal::warning(m);
    pyre::libjournal::error(m);

    // convenience functions at module level
    pyre::libjournal::api(m);
}


// end of file
