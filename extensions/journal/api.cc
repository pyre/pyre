// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings to the inventory
void
pyre::journal::py::api(py::module & m)
{
    // easy access to the manager of the global state
    m.attr("chronicler") = m.attr("Chronicler");

    // registration of the application name
    m.def(
        "application",
        // the implementation
        &pyre::journal::application, "name"_a,
        // the docstring
        "register the application {name}");

    // suppress all output
    m.def(
        "quiet",
        // the implementation
        &pyre::journal::quiet,
        // the docstring
        "suppress all channel output");

    // send output to a log file
    m.def(
        "logfile",
        // the implementation
        [](const debug_t::string_type & path) { pyre::journal::logfile(path); },
        // the docstring
        "send all output to a file",
        // the arguments
        "name"_a);

    // set the maximum message decoration level
    m.def(
        "decor",
        // the implementation
        [](chronicler_t::detail_type level) { chronicler_t::decor(level); },
        // the docstring
        "set the maximum message decoration level",
        // the arguments
        "level"_a);

    // set the maximum message detail level
    m.def(
        "detail",
        // the implementation
        [](chronicler_t::detail_type level) { chronicler_t::detail(level); },
        // the docstring
        "set the maximum message detail level",
        // the arguments
        "level"_a);

    // all done
    return;
}


// end of file
