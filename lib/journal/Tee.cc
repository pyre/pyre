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
#include "Device.h"
#include "Splitter.h"
#include "Console.h"
#include "File.h"
// my declarations
#include "Tee.h"


// metamethods
// a tee to the console and to a file at each of the given {paths}
pyre::journal::Tee::Tee(const paths_type & paths, const name_type & name) : super_type(name)
{
    // the console comes first
    attach(std::make_shared<Console>());
    // then a file at each path
    for (const auto & path : paths) {
        // that opens for writing
        attach(std::make_shared<File>(path));
    }
    // all done
    return;
}


// destructor
pyre::journal::Tee::~Tee() {}


// end of file
