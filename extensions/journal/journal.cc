// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// helpers
#include "helpers.h"


// the module entry point
PYBIND11_MODULE(journal, m)
{
    // the doc string
    m.doc() = "the journal extension module";

    // register the exception types
    pyre::journal::py::exceptions(m);

    // journal entry parts
    pyre::journal::py::entry(m);

    // global state
    pyre::journal::py::chronicler(m);
    // devices
    pyre::journal::py::devices(m);
    // developer channels
    pyre::journal::py::debug(m);
    pyre::journal::py::firewall(m);
    // user facing channels
    pyre::journal::py::info(m);
    pyre::journal::py::warning(m);
    pyre::journal::py::error(m);
    pyre::journal::py::help(m);

    // convenience functions at module level
    pyre::journal::py::api(m);
}


// end of file
