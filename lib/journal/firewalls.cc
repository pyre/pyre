// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include <cstdarg>
// the journal interface
#include "public.h"
// my declarations
#include "firewalls.h"


// type alias
using firewall_t = pyre::journal::firewall_t;


// hit
extern "C" void
firewall_hit(const char * channel, __HERE_DECL__, const char * fmt, ...)
{
    // pull the varargs
    std::va_list args;
    char buffer[4096];
    va_start(args, fmt);
    std::vsnprintf(buffer, sizeof(buffer), fmt, args);
    va_end(args);

    // create a firewall channel
    firewall_t firewall(channel);

    // render the line number, leaving it blank when it is unknown
    auto line = lineno > 0 ? std::to_string(lineno) : "";
    // log the message
    firewall << pyre::journal::Locator(filename, line, funcname) << buffer << pyre::journal::endl;

    // all done
    return;
}


// check
extern "C" void
firewall_check(const char * channel, int condition, __HERE_DECL__, const char * fmt, ...)
{
    // if {condition} is false
    if (!condition) {
        // pull the varargs
        std::va_list args;
        char buffer[4096];
        va_start(args, fmt);
        std::vsnprintf(buffer, sizeof(buffer), fmt, args);
        va_end(args);

        // create a firewall channel
        firewall_t firewall(channel);

        // render the line number, leaving it blank when it is unknown
        auto line = lineno > 0 ? std::to_string(lineno) : "";
        // log the message
        firewall << pyre::journal::Locator(filename, line, funcname) << buffer
                 << pyre::journal::endl;
    }

    // all done
    return;
}


// end of file
