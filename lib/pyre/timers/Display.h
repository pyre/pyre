// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//


#if !defined(pyre_timers_Display_h)
#define pyre_timers_Display_h


// The class Display is a wrapper around Timer that adds the ability to assign names to timers
// and register them with a local registry. Clients can retrieve timer instances by name, so
// that timer control can be accomplished throughout and application without having to pass
// timer instances around.

// place me in the proper namespace
namespace pyre {
    namespace timers {
        class Display;
    }
}

// imported types
#include <string>
#include "Timer.h"
#include <pyre/patterns/Registrar.h>

// declaration
class pyre::timers::Display {
    // types
public:
    typedef std::string name_t;
    typedef Timer timer_t;
    typedef pyre::patterns::Registrar<timer_t> index_t;

    // interface
public:
    name_t name() const;
    // start a timer
    Display & start();
    // stop a timer
    Display & stop();
    // zero out a timer
    Display & reset();

    // take a reading in seconds from a *running* timer
    double lap();
    // get the number of seconds accumulated by a *stopped* timer
    double read();

    // locate a timer given its name
    static timer_t & retrieveTimer(name_t name);

    // meta methods
public:
    virtual ~Display();
    inline Display(name_t name);

    // data members
private:
    timer_t & _timer;

    static index_t _index;

    // implementation details
private:
};

// get the inline definitions
#define pyre_timers_Display_icc
#include "Display.icc"
#undef pyre_timers_Display_icc

#endif

// end of file
