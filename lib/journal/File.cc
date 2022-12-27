// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// external support
#include "externals.h"
// get the forward declarations
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
// get the file declaration
#include "File.h"


// metamethods
// destructor
pyre::journal::File::~File() {}


// interface
auto
pyre::journal::File::alert(const entry_type & entry) -> File &
{
    // get the page and the notes
    auto & page = entry.page();
    auto & notes = entry.notes();

    // if there is no payload and no metadata
    if (page.empty() && notes.empty()) {
        // nothing else to do
        return *this;
    }

    // otherwise, get the alert renderer to format the message
    auto content = _alert->render(_palette, entry);
    // inject it into my file
    _file << content;

    // all done
    return *this;
}


auto
pyre::journal::File::help(const entry_type & entry) -> File &
{
    // get the memo renderer to format the message
    auto content = _help->render(_palette, entry);
    // inject it into my file
    _file << content;
    // all done
    return *this;
}


auto
pyre::journal::File::memo(const entry_type & entry) -> File &
{
    // get the memo renderer to format the message
    auto content = _memo->render(_palette, entry);
    // inject it into my file
    _file << content;
    // all done
    return *this;
}


// end of file
