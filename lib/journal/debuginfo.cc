// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include <cstdarg>
// the journal interface
#include "public.h"
// my declarations
#include "debuginfo.h"

// type alias
using debug_t = pyre::journal::debug_t;


// check the state
extern "C" int
debuginfo_active(const char * name)
{
    // make the channel
    return debug_t(name).active();
}


// activate a channel
extern "C" void
debuginfo_activate(const char * name)
{
    // make the channel and activate it
    debug_t(name).activate();
    // all done
    return;
}


// deactivate a channel
extern "C" void
debuginfo_deactivate(const char * name)
{
    // make the channel and deactivate it
    debug_t(name).deactivate();
    // all done
    return;
}


// send a message to the default device
extern "C" void
debuginfo_out(const char * name, __HERE_DECL__, const char * fmt, ...)
{
    // build the channel
    debug_t channel(name);

    // if the channel is active
    if (channel) {
        // make a (large enough?) buffer
        char buffer[4096];
        // pull the varargs
        std::va_list args;
        va_start(args, fmt);
        std::vsnprintf(buffer, sizeof(buffer), fmt, args);
        va_end(args);

        // log the message
        channel << pyre::journal::locator_t(__HERE_ARGS__) << buffer << pyre::journal::endl;
    }

    // all done
    return;
}


// end of file
