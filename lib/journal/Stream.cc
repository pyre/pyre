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
// get the stream declaration
#include "Stream.h"


// metamethods
// destructor
pyre::journal::Stream::~Stream() {}


// interface
auto
pyre::journal::Stream::alert(const entry_type & entry) -> Stream &
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
    // inject it into my stream
    _stream << content;

    // all done
    return *this;
}


auto
pyre::journal::Stream::help(const entry_type & entry) -> Stream &
{
    // get the memo renderer to format the message
    auto content = _help->render(_palette, entry);
    // inject it into my stream
    _stream << content;
    // all done
    return *this;
}


auto
pyre::journal::Stream::memo(const entry_type & entry) -> Stream &
{
    // get the memo renderer to format the message
    auto content = _memo->render(_palette, entry);
    // inject it into my stream
    _stream << content;
    // all done
    return *this;
}


// end of file
