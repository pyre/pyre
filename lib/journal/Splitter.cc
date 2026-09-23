// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external support
#include "externals.h"
// forward declarations
#include "forward.h"
// type aliases
#include "api.h"

// get the support i need
#include "Entry.h"
// my superclass
#include "Device.h"
// my declarations
#include "Splitter.h"


// metamethods
pyre::journal::Splitter::~Splitter() {}


// interface
// user facing messages
auto
pyre::journal::Splitter::alert(const entry_type & entry) -> Splitter &
{
    // go through my devices
    for (auto & output : _outputs) {
        // and hand each one the entry
        output->alert(entry);
    }
    // all done
    return *this;
}


// help messages
auto
pyre::journal::Splitter::help(const entry_type & entry) -> Splitter &
{
    // go through my devices
    for (auto & output : _outputs) {
        // and hand each one the entry
        output->help(entry);
    }
    // all done
    return *this;
}


// developer messages
auto
pyre::journal::Splitter::memo(const entry_type & entry) -> Splitter &
{
    // go through my devices
    for (auto & output : _outputs) {
        // and hand each one the entry
        output->memo(entry);
    }
    // all done
    return *this;
}


// end of file
