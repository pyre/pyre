// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//


// for the build system
#include <portinfo>

// external packages
#include <map>
#include <vector>
#include <string>
#include <sstream>
#include <cstdlib>

// local types
#include "Device.h"
#include "Chronicler.h"
#include "Inventory.h"
#include "Index.h"
#include "Channel.h"
// diagnostics
#include "Diagnostic.h"
#include "Debug.h"
#include "Error.h"
#include "Firewall.h"
#include "Informational.h"
#include "Warning.h"

// type aliases
typedef std::string string_t;

// initialization routines
static pyre::journal::Debug::index_t initializeDebugIndex()
{
    // instantiate the map
    pyre::journal::Debug::index_t channels;
    // read the magic environment variable
    const char * var = std::getenv("DEBUG_OPT");
    // if set
    if (var) {
        // convert it into a string
        string_t setting(var);
        // the channels are delimited by colons
        string_t delimiter = ":";
        // declare a couple of cursor to assist with the scanning
        string_t::size_type last;
        string_t::size_type first = setting.find_first_not_of(delimiter);
        // scan away...
        while (first != string_t::npos) {
            // find the end of the current token
            last = setting.find_first_of(delimiter, first);
            // extract the channel name
            string_t channel = setting.substr(first, last-first);
            // and activate it
            channels.lookup(channel) = true;
            // position the scanner to the beginning of the next token
            first = setting.find_first_not_of(delimiter, last);
        }
    }

    return channels;
}


// specializations that serve as definitions of the indices
namespace pyre {
    namespace journal {
        // define the indices
        Firewall::index_t Firewall::_index = Firewall::index_t();
        Debug::index_t Debug::_index = initializeDebugIndex();
        Error::index_t Error::_index = Error::index_t();
        Warning::index_t Warning::_index = Warning::index_t();
        Informational::index_t Informational::_index = Informational::index_t();
    }
}

// end of file
