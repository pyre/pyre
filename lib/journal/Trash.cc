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
// message contents
#include "Entry.h"

// renderer support
#include "Renderer.h"
#include "Alert.h"
#include "Bland.h"
#include "Memo.h"

// my superclass
#include "Device.h"
// get the stream declaration
#include "Trash.h"


// metamethods
// destructor
pyre::journal::Trash::~Trash() {}


// interface
auto
pyre::journal::Trash::alert(const entry_type & entry) -> Trash &
{
    // make an empty palette
    palette_type palette;
    // go through the motions, and then discard the content
    _alert->render(palette, entry);
    // all done
    return *this;
}


auto
pyre::journal::Trash::help(const entry_type & entry) -> Trash &
{
    // make an empty palette
    palette_type palette;
    // go through the motions, and then discard the content
    _help->render(palette, entry);
    // all done
    return *this;
}


auto
pyre::journal::Trash::memo(const entry_type & entry) -> Trash &
{
    // make an empty palette
    palette_type palette;
    // go through the motions, and then discard the content
    _memo->render(palette, entry);
    // all done
    return *this;
}


// end of file
