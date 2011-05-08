// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 


// for the build system
#include <portinfo>

// external packages
#include <map>
#include <vector>
#include <string>

// local types
#include "Inventory.h"
#include "Index.h"
#include "Channel.h"
#include "Device.h"
#include "Renderer.h"
#include "Chronicler.h"


// simplify access to the pyre::journal symbols
using namespace pyre::journal;


// implementation of {Chronicler}
// definition of the static methods
pyre::journal::Chronicler::journal_t &
pyre::journal::Chronicler::
journal()
{
    // N.B.: this only happens once!
    static journal_t * _journal 
        = new journal_t(
                        // the default device is the console
                        0,
                        // build a new default renderer
                        new Renderer());
    // return the static instance
    return *_journal;
}


// end of file
