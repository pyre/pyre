// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved

// code guard
#if !defined(pyre_journal_public_h)
#define pyre_journal_public_h


// external packagesvap
#include "externals.h"
// get the forward declarations
#include "forward.h"

// published type aliases; this is the file you are looking for...
#include "api.h"

// exceptions
#include "exceptions.h"

// global settings
#include "Chronicler.h"

// message entry
#include "Entry.h"
// message metadata
#include "Verbosity.h"
#include "Locator.h"
#include "Note.h"
#include "Flush.h"

// abstractions
#include "Renderer.h"
#include "Device.h"

// renderers
#include "Alert.h"
#include "Memo.h"

// devices
#include "Splitter.h"
#include "Trash.h"
#include "File.h"
#include "Stream.h"
#include "Console.h"
#include "ErrorConsole.h"

// support for channel shared state
#include "Inventory.h"
#include "InventoryProxy.h"
#include "Index.h"

// channel infrastructure
#include "Channel.h"

// channels
#include "Null.h"
// end user facing
#include "Informational.h"
#include "Warning.h"
#include "Error.h"
// developer facing
#include "Debug.h"
#include "Firewall.h"

// manipulators
#include "manipulators.h"

// terminal support
#include "ASCII.h"
#include "CSI.h"
#include "ANSI.h"


// the convenience initializer
void
pyre::journal::
init(int argc, char* argv[])
{
    // ask {chronicler} to do this
    pyre::journal::chronicler_t::init(argc, argv);
    // all done
    return;
}


// register the application name with the chronicler
void
pyre::journal::
application(const value_t & name)
{
    // get the global metadata
    auto & notes = chronicler_t::notes();
    // register the given name under the {application} key; the key is guaranteed to exist:
    // it's part of the {chronicler_t} initialization
    notes.at("application") = name;
    // all done
    return;
}


// install the trash can as the global device
void
pyre::journal::
quiet()
{
    // forward to the {chronicler_t}
    chronicler_t::quiet();
    // all done
    return;
}


// send all channel output to a log file
void
pyre::journal::
logfile(const path_t & name)
{
    // create the device and register it with the chronicler
    chronicler_t::device<file_t>(name);
    // all done
    return;
}


#endif

// end of file
