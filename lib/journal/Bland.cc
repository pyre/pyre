// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


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
#include "Bland.h"


// metamethods
pyre::journal::Bland::~Bland() {}


// implementation details
void
pyre::journal::Bland::header(
    palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // nothing to do
    return;
}


void
pyre::journal::Bland::body(
    palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();

    // go through the lines in the page
    for (auto line : page) {
        // and render each one
        buffer << "  " << line << std::endl;
    }

    return;
}


void
pyre::journal::Bland::footer(
    palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // nothing to do
    return;
}


// end of file
