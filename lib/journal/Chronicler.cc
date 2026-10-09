// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


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
#include "Splitter.h"
#include "Courier.h"

// access to {debug_t}
// channel parts
#include "Inventory.h"
#include "InventoryProxy.h"
#include "Index.h"
#include "Channel.h"
// the {debug} channel
#include "Debug.h"
// the rest of the severities, whose devices get swept
#include "Firewall.h"
#include "Informational.h"
#include "Warning.h"
#include "Error.h"
#include "Help.h"


// aliases
using console_t = pyre::journal::cout_t;
using chronicler_t = pyre::journal::chronicler_t;
using splitter_t = pyre::journal::splitter_t;
using courier_t = pyre::journal::courier_t;


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

    // go through the arguments
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


// detach every foreign device from the journal
void
chronicler_t::detachForeign()
{
    // the devices already examined, so that shared and circular arrangements are walked once
    visited_type visited;
    // if the default device is foreign
    if (_device && _device->foreign()) {
        // replace it with a console, since every channel falls back on it
        _device = std::make_shared<console_t>();
    }
    // otherwise
    else {
        // detach the foreign devices it forwards entries to
        prune(_device, visited);
    }
    // sweep the developer channels, whether or not they are live in this build
    sweepIndex(Debug<InventoryProxy>::index(), visited);
    sweepIndex(Firewall<InventoryProxy>::index(), visited);
    // and the user facing ones
    sweepIndex(Informational<InventoryProxy>::index(), visited);
    sweepIndex(Warning<InventoryProxy>::index(), visited);
    sweepIndex(Error<InventoryProxy>::index(), visited);
    sweepIndex(Help<InventoryProxy>::index(), visited);
    // all done
    return;
}


// detach the foreign devices from the default of a severity and from each of its channels
void
chronicler_t::sweepIndex(index_type & index, visited_type & visited)
{
    // start with the default device of the severity
    sweepInventory(index, visited);
    // go through its channels
    for (auto & [name, inventory] : index) {
        // and sweep each one
        sweepInventory(inventory, visited);
    }
    // all done
    return;
}


// detach a foreign device from the shared state of a channel
void
chronicler_t::sweepInventory(inventory_type & inventory, visited_type & visited)
{
    // get the device
    auto device = inventory.device();
    // if it is foreign
    if (device && device->foreign()) {
        // forget it, so the channel falls back on the device above it
        inventory.device(nullptr);
        // and we are done
        return;
    }
    // otherwise, detach the foreign devices it forwards entries to
    prune(device, visited);
    // all done
    return;
}


// detach the foreign devices among those a device forwards entries to
void
chronicler_t::prune(const device_type & device, visited_type & visited)
{
    // if there is no device, or it has been examined already
    if (!device || !visited.insert(device.get()).second) {
        // there is nothing to do
        return;
    }
    // if it is a splitter
    if (auto splitter = std::dynamic_pointer_cast<splitter_t>(device)) {
        // copy its outputs, since detaching modifies them
        auto outputs = splitter->outputs();
        // go through them
        for (const auto & output : outputs) {
            // if this one is foreign
            if (output && output->foreign()) {
                // detach it
                splitter->detach(output);
                // and move on
                continue;
            }
            // otherwise, detach the foreign devices it forwards entries to
            prune(output, visited);
        }
        // and we are done
        return;
    }
    // if it is a courier
    if (auto courier = std::dynamic_pointer_cast<courier_t>(device)) {
        // get its mirror
        auto mirror = courier->mirror();
        // if the mirror is foreign
        if (mirror && mirror->foreign()) {
            // stop the mirroring
            courier->mirror(nullptr);
            // and we are done
            return;
        }
        // otherwise, detach the foreign devices the mirror forwards entries to
        prune(mirror, visited);
        // and we are done
        return;
    }
    // all done
    return;
}


// data
chronicler_t::margin_type chronicler_t::_margin = { "  " };
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
