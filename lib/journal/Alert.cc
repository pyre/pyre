// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// external support
#include "externals.h"
// forward declarations
#include "forward.h"
// type aliases
#include "api.h"

// the global settings
#include "Chronicler.h"
// message contents
#include "Entry.h"
// the superclass
#include "Renderer.h"
// the declaration
#include "Alert.h"


// metamethods
pyre::journal::Alert::
~Alert()
{}


// implementation details
void
pyre::journal::Alert::
header(palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();
    // if there is nothing to print
    if (page.empty()) {
        // we are done
        return;
    }

    // get the notes
    auto & notes = entry.notes();

    // get the severity
    auto severity = notes.at("severity");
    // ask the palette for the severity decoration
    auto severityColor = palette[severity];
    // if we are generating color output
    if (!severityColor.empty()) {
        // print the application name in the correct color
        buffer
            << severityColor << notes.at("application") << palette["reset"];
    } else {
        // otherwise, print the application name, followed by the severity
        buffer
            << notes.at("application") << "(" << notes.at("severity") << ")";
    }

    // make some space, and print the first line of the body
    buffer
        << ": "
        << palette["body"] << page[0] << palette["reset"]
        << std::endl;

    // all done
    return;
}


void
pyre::journal::Alert::
body(palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();

    // the page had up to one line
    if (page.size() < 2) {
        // we have rendered the first line already; nothing further to do
        return;
    }
    // go through the lines in the page; skip the first one, since it was printed as part of
    // the header
    for (auto line = page.begin()+1; line != page.end(); ++line) {
        // and render them
        buffer
            << palette["body"] << (*line) << palette["reset"]
            << std::endl;
    }

    // all done
    return;
}


// end of file
