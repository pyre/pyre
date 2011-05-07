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

using namespace pyre::journal;

// convenience
typedef Inventory<true> true_t;
typedef Inventory<false> false_t;

// must subclass since the Channel constructor and destructor are protected
class trueref_t : public Channel<trueref_t> {
public:
    trueref_t(string_t name) : Channel<trueref_t>::Channel(name) {}
};

class falseref_t : public Channel<falseref_t, false> {
public:
    falseref_t(string_t name) : Channel<falseref_t,false>::Channel(name) {}
};


// specializations for the static data members
template<> typename trueref_t::index_t Channel<trueref_t>::_index = trueref_t::index_t();
template<> typename falseref_t::index_t Channel<falseref_t,false>::_index = falseref_t::index_t();

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
