// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the debug channel
void
pyre::journal::py::entry(py::module & m)
{
    // journal entry body
    py::bind_vector<pyre::journal::page_t>(m, "Page");
    // journal entry metadata
    py::bind_map<pyre::journal::notes_t>(m, "Notes");

    // journal entries
    auto cls = py::class_<entry_t>(m, "Entry");
    // parts
    cls.def_property_readonly(
        // the name
        "page",
        // the implementation
        py::overload_cast<>(&entry_t::page, py::const_),
        // the docstring
        "retrieve the body of this entry");

    cls.def_property_readonly(
        // the name
        "notes",
        // the implementation
        py::overload_cast<>(&entry_t::notes, py::const_),
        // the docstring
        "retrieve the notes of this entry");

    // all done
    return;
}


// end of file
