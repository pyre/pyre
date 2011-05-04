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
#include <string>
#include <cstdlib>

// local types
#include "Inventory.h"
#include "Index.h"
#include "Channel.h"
#include "Diagnostic.h"
#include "Debug.h"


// type aliases
typedef std::string string_t;

typedef pyre::journal::Debug debug_t;
typedef debug_t::index_t debugindex_t;


// initialization routines
static debugindex_t initializeDebugIndex()
{
    // instantiate the map
    debugindex_t channels;
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
template <>
debugindex_t 
debug_t::channel_t::_index = initializeDebugIndex();


// end of file
