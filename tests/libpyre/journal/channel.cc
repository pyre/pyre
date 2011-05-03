// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


// for the build system
#include <portinfo>

// packages
#include <assert.h>
#include <map>
#include <string>

// access to the low level inventory header file
#include <pyre/journal/Inventory.h>
#include <pyre/journal/Index.h>
#include <pyre/journal/Channel.h>

class Debug {};

// convenience
typedef pyre::journal::Inventory<true> true_t;
typedef pyre::journal::Inventory<false> false_t;

typedef pyre::journal::Channel<Debug> trueref_t;
typedef pyre::journal::Channel<Debug, false> falseref_t;


// specializations for the static data members
template<> typename trueref_t::index_t trueref_t::_index = trueref_t::index_t();
template<> typename falseref_t::index_t falseref_t::_index = falseref_t::index_t();

// main program
int main() {

    // and wrap channels over them
    trueref_t on_ref("true");
    falseref_t off_ref("true");

    // check their default settings
    assert(on_ref.isActive() == true);
    assert(off_ref.isActive() == false);

    // flip them
    on_ref.deactivate();
    off_ref.activate();

    // check again
    assert(on_ref.isActive() == false);
    assert(off_ref.isActive() == true);

    // all done
    return 0;
}

// end of file
