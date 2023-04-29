// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_py_forward_h)
#define pyre_journal_py_forward_h


// get the helpers
#include "helpers.h"

// the {libjournal} namespace
namespace pyre::journal::py {

    // exceptions
    void exceptions(py::module &);

    // module level convenience methods
    void api(py::module &);

    // journal entry parts
    void entry(py::module &);

    // module methods
    void chronicler(py::module &);
    void devices(py::module &);

    // developer channels
    void debug(py::module &);
    void firewall(py::module &);
    // user facing channels
    void info(py::module &);
    void warning(py::module &);
    void error(py::module &);
    void help(py::module &);
} // namespace pyre::journal::py


#endif

// end of file
