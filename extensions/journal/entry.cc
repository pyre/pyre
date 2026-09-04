// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


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
    // constructor
    cls.def(
        // the implementation: an entry with the given content, for those that rebuild entries
        // from records; the containers may be native or bound, so convert element by element
        py::init([](py::iterable page, py::object notes) {
            // make an entry
            auto entry = std::make_unique<entry_t>();
            // fill its page
            for (auto line : page) {
                // one line at a time
                entry->page().push_back(py::cast<string_t>(line));
            }
            // the record notes are authoritative; start clean
            entry->notes().clear();
            // and fill them in
            for (auto item : notes.attr("items")()) {
                // unpack each pair
                auto pair = py::cast<py::tuple>(item);
                // and store it
                entry->notes()[py::cast<string_t>(pair[0])] = py::cast<string_t>(pair[1]);
            }
            // hand it off
            return entry;
        }),
        // the signature
        "page"_a, "notes"_a,
        // the docstring
        "build an entry with the given {page} and {notes}");
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
