// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// external support
#include "externals.h"
// forward declarations
#include "forward.h"
// type aliases
#include "api.h"

// get the declaration
#include "Chronicler.h"

// infrastructure needed by the initializers
#include "exceptions.h"
// message content
#include "Entry.h"
// access to the console and the trash can
// renderer support
#include "Renderer.h"
#include "Alert.h"
#include "Bland.h"
#include "Memo.h"
// device support
#include "Device.h"
#include "File.h"
#include "Stream.h"
#include "Console.h"
#include "Trash.h"

// access to {debug_t}
// channel parts
#include "Inventory.h"
#include "InventoryProxy.h"
#include "Index.h"
#include "Channel.h"
// the {debug} channel
#include "Debug.h"


// aliases
using console_t = pyre::journal::cout_t;
using chronicler_t = pyre::journal::chronicler_t;


// helpers
static auto
initializeGlobals() -> chronicler_t::notes_type;

static auto
initializeDecor() -> chronicler_t::detail_type;

static auto
initializeDetail() -> chronicler_t::detail_type;

// the initializer
void
chronicler_t::init(int argc, char * argv[])
{
    // our marker
    string_type marker("--journal.");
    // the table of parsed arguments
    cmd_type commands;

    // go trough the arguments
    for (int i = 0; i < argc; ++i) {
        // convert into a string
        string_type arg(argv[i]);
        // filter the ones that are for me
        if (arg.compare(0, marker.size(), marker) == 0) {
            // extract the command
            auto cmd = arg.substr(marker.size());
            // split on the equal sign
            auto sep = cmd.find("=");
            // extract the name part
            auto name = cmd.substr(0, sep);
            // and the value part
            auto value = (sep != string_t::npos) ? cmd.substr(sep + 1, string_t::npos) : "";
            // put them in the table
            commands[name] = value;
        }
    }

    // check for decor
    const auto & decoLevel = commands["decor"];
    // if there
    if (!decoLevel.empty()) {
        // attempt to
        try {
            // extract and set it
            decor(std::stoi(decoLevel));
        }
        // if anything goes wrong
        catch (...) {
            // ignore it
        }
    }

    // check for detail
    const auto & detailLevel = commands["detail"];
    // if there
    if (!detailLevel.empty()) {
        // attempt to
        try {
            // extract and set it
            detail(std::stoi(detailLevel));
        }
        // if anything goes wrong
        catch (...) {
            // ignore it
        }
    }

    // check for debug channels
    auto & debug = commands["debug"];
    // if there
    if (!debug.empty()) {
        // convert the comma separated list into a set of channel names
        auto channels = nameset(debug);
        // ask the debug channel to activate these
        debug_t::activateChannels(channels);
    }

    // all dome
    return;
}


// suppress all output
void
chronicler_t::quiet()
{
    // make a trash can and install it as the default device
    device<trash_t>();
    // all done
    return;
}


// data
chronicler_t::margin_type chronicler_t::_margin = { "    " };
chronicler_t::detail_type chronicler_t::_decor { initializeDecor() };
chronicler_t::detail_type chronicler_t::_detail { initializeDetail() };
chronicler_t::notes_type chronicler_t::_notes { initializeGlobals() };
chronicler_t::device_type chronicler_t::_device { std::make_shared<console_t>() };


// implementation details
auto
initializeGlobals() -> chronicler_t::notes_type
{
    // make a table
    chronicler_t::notes_type table;

    // initialize the expected metadata with default values; applications are expected to
    // replace these with values that are more sensible
    table["application"] = "journal";

    // return it
    return table;
}


auto
initializeDecor() -> chronicler_t::detail_type
{
    // establish the default decor level
    chronicler_t::detail_type level = 1;

    // try to read the {JOURNAL_DECOR} environment variable
    const char * setting = std::getenv("JOURNAL_DECOR");
    // if there
    if (setting != nullptr) {
        // attempt to convert to a {detail_t}
        auto status = std::strtol(setting, nullptr, 10);
        // if the conversion succeeded
        if (status != 0) {
            // save it
            level = status;
        }
    }

    // return the detail level; note that this implementation makes it impossible to set
    // its value to zero from the environment
    return level;
}


auto
initializeDetail() -> chronicler_t::detail_type
{
    // establish the default severity level
    chronicler_t::detail_type level = 1;

    // try to read the {JOURNAL_DETAIL} environment variable
    const char * setting = std::getenv("JOURNAL_DETAIL");
    // if there
    if (setting != nullptr) {
        // attempt to convert to a {detail_t}
        auto status = std::strtol(setting, nullptr, 10);
        // if the conversion succeeded
        if (status != 0) {
            // save it
            level = status;
        }
    }

    // return the detail level; note that this implementation makes it impossible to set
    // its value to zero from the environment
    return level;
}


// end of file
