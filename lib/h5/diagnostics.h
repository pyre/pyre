// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once

// stdlib
#include <source_location>
#include <string>
// external packages
#include "external.h"
// set up the namespace
#include "forward.h"


// the reporting of library refusals
//
// every call into the hdf5 library answers with a status, or with a handle that is invalid on
// failure, and a refusal leaves the library's reasons on an error stack of its own that the
// caller never sees. the functions here turn a refusal into one journal entry on a channel
// named for the area of the library that was asked: where the call was made, what it was
// trying to do, and the library's own explanation. callers test the status, complain, and
// hand back a safe default; nothing here throws
namespace pyre::h5 {
    // the library's explanation of its latest refusal: the innermost frame of its error stack,
    // as the function that refused and its reason, or an empty string when the stack is clean
    auto explanation() -> std::string;

    // report a refusal on the channel called {channel}: what the caller was attempting, in the
    // form of a gerund phrase, followed by what the library has to say about it. the library's
    // explanation is read here, so the attempt text must not itself call into the library:
    // every call clears the error stack
    void complain(
        const char * channel, const std::string & attempt,
        const std::source_location location = std::source_location::current());

    // the same report, with the library's explanation collected by the caller ahead of time;
    // for attempts whose text asks the library for something, e.g. the name of the object,
    // which would wipe the explanation before it is read
    void complain(
        const char * channel, const std::string & attempt, const std::string & reason,
        const std::source_location location = std::source_location::current());
} // namespace pyre::h5


// end of file
