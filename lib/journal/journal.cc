// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2012 all rights reserved
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

// firewall
typedef pyre::journal::Firewall firewall_t;
typedef firewall_t::index_t firewallindex_t;
// debug
typedef pyre::journal::Debug debug_t;
typedef debug_t::index_t debugindex_t;
// error
typedef pyre::journal::Error error_t;
typedef error_t::index_t errorindex_t;
// informational
typedef pyre::journal::Informational info_t;
typedef info_t::index_t infoindex_t;
// warning
typedef pyre::journal::Warning warning_t;
typedef warning_t::index_t warningindex_t;


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
// firewall
template <>
firewallindex_t 
firewall_t::channel_t::_index = firewallindex_t();

// debug
template <>
debugindex_t 
debug_t::channel_t::_index = initializeDebugIndex();

// error
template <>
errorindex_t 
error_t::channel_t::_index = errorindex_t();

// info
template <>
infoindex_t 
info_t::channel_t::_index = infoindex_t();

// warning
template <>
warningindex_t 
warning_t::channel_t::_index = warningindex_t();


// end of file
