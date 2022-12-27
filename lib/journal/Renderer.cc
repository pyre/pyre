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

// global settings
#include "Chronicler.h"
// message content
#include "Entry.h"
// the base device
#include "Device.h"

// get the declaration
#include "Renderer.h"


// metamethods
pyre::journal::Renderer::
~Renderer()
{}


// interface
auto
pyre::journal::Renderer::
render(palette_type & palette, const entry_type & entry) const -> line_type
{
    // make a buffer
    linebuf_type buffer;

    // build the document
    header(palette, buffer, entry);
    body(palette, buffer, entry);
    footer(palette, buffer, entry);

    // extract the string and return it
    return buffer.str();
}


// implementation details
void
pyre::journal::Renderer::
header(palette_type &, linebuf_type &, const entry_type &) const
{
    // all done
    return;
}


void
pyre::journal::Renderer::
body(palette_type &, linebuf_type &, const entry_type &) const
{
    // all done
    return;
}


void
pyre::journal::Renderer::
footer(palette_type &, linebuf_type &, const entry_type &) const
{
    // all done
    return;
}


// end of file
