// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// get the journal
#include <pyre/journal.h>

// pybind support
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

// make certain STL containers opaque
PYBIND11_MAKE_OPAQUE(pyre::journal::page_t);
PYBIND11_MAKE_OPAQUE(pyre::journal::notes_t);


// type aliases
namespace pyre::libjournal {
    // from the standard library
    using string_t = std::string;


    // from {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals
    using namespace py::literals;


    // from {pyre::journal}
    // the exceptions
    using debug_error = pyre::journal::debug_error;
    using firewall_error = pyre::journal::firewall_error;
    using application_error = pyre::journal::application_error;

    // the global state
    using chronicler_t = pyre::journal::chronicler_t;

    // devices
    using device_t = pyre::journal::device_t;
    using trash_t = pyre::journal::trash_t;
    using stream_t = pyre::journal::stream_t;
    using cout_t = pyre::journal::cout_t;
    using cerr_t = pyre::journal::cerr_t;

    // channels
    using debug_t = pyre::journal::debug_t;
    using firewall_t = pyre::journal::firewall_t;
    using info_t = pyre::journal::info_t;
    using warning_t = pyre::journal::warning_t;
    using error_t = pyre::journal::error_t;
}


// end of file
