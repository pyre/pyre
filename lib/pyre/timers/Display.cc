// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// for the build system
#include <portinfo>

// my header
#include "Display.h"

// quick access to my namespace
using namespace pyre::timers;

// the map
Display::index_t Display::_index;


// lookup a timer in the index and return it
Display::timer_t & Display::retrieveTimer(name_t name) {
    //
    // lookup <name> in the _index and return the associated timer
    // if not found, create a new one and index it under <name>
    timer_t * timer;
    // try to find the timer associated with this name in the index
    index_t::iterator lookup = _index.find(name);
    // if it's there grab it; otherwise build a new and add it to the container
    if (lookup != _index.end()) {
        timer = lookup->second;
    } else {
        timer = new timer_t(name);
        _index[name] = timer;
    }
    // and return a reference to the timer
    return *timer;
}


// destructor
Display::~Display() {}

// end of file
