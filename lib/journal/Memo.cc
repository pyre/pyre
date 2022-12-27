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

// the global settings
#include "Chronicler.h"
// message contents
#include "Entry.h"
// the superclass
#include "Renderer.h"
// the declaration
#include "Memo.h"


// metamethods
pyre::journal::Memo::~Memo() {}


// implementation details
void
pyre::journal::Memo::header(
    palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();
    // if there are no contents
    if (page.empty()) {
        // we are done
        return;
    }

    // get the notes
    auto & notes = entry.notes();
    // get the channel severity
    auto severity = notes.at("severity");
    // and its name
    auto channel = notes.at("channel");

    // attempt to get location information
    // N.B.: we only print line number and function name if we know the filename
    auto loc = notes.find("filename");
    // if it's there
    if (loc != notes.end()) {
        // extract the filename
        auto filename = loc->second;
        // make some room and turn on location formatting
        buffer << palette[severity];
        // set a maximum length for the rendered filename
        const line_type::size_type maxlen = 60;
        // get the filename size
        auto len = filename.size();
        // so that names that are longer than this maximum
        if (len > maxlen) {
            // get shortened
            buffer << filename.substr(0, maxlen / 4 - 3) << "..."
                   << filename.substr(len - 3 * maxlen / 4);
        } else {
            // otherwise, render the whole name
            buffer << filename;
        }
        // reset the buffer and add a spacer
        buffer << palette["reset"] << ":";

        // attempt to get the line number
        auto & line = notes.at("line");
        // if we know it
        if (!line.empty()) {
            // render it
            buffer << palette[severity] << line << palette["reset"] << ":";
        }

        // same with the function name
        auto & function = notes.at("function");
        // if we know it
        if (!function.empty()) {
            // render it
            buffer << palette[severity] << " " << function << palette["reset"] << ":";
        }
        // wrap up the location info
        buffer << std::endl;
    }
    // if we don't have location information
    else {
        // we show some basic channel information instead
        buffer
            // print the severity
            << palette[severity] << severity << palette["reset"] << ":" << std::endl;

        // at the correct {decor} level
        if (chronicler_t::decor() > 1) {
            // print
            buffer
                // a marker
                << palette[severity] << _headerMarker
                << palette["reset"]
                // and a warning that there is no location information
                << "location information is not available"
                // done
                << std::endl;
        }
    }

    // all done
    return;
}


void
pyre::journal::Memo::body(
    palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();
    // if the page is empty
    if (page.empty()) {
        // nothing to do
        return;
    }

    // get the notes
    auto & notes = entry.notes();
    // get the channel severity
    auto severity = notes.at("severity");

    // go through the lines in the page
    for (auto & line : page) {
        // and render them
        buffer << palette[severity] << _bodyMarker << palette["reset"] << palette["body"] << line
               << palette["reset"] << std::endl;
    }

    // all done
    return;
}


void
pyre::journal::Memo::footer(
    palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();
    // if the page is empty
    if (page.empty()) {
        // nothing to do
        return;
    }

    // get the notes
    auto & notes = entry.notes();
    // get the channel severity
    auto severity = notes.at("severity");
    // and its name
    auto channel = notes.at("channel");

    if (chronicler_t::decor() > 2) {
        // look for the application name
        auto loc = notes.find("application");
        // if it's there
        if (loc != notes.end()) {
            // get the value
            auto app = loc->second;
            // render the app name
            buffer
                // first a marker
                << palette[severity] << _footerMarker
                << palette["reset"]
                // inject the application name
                << "from application " << palette[severity] << app
                << palette["reset"]
                // done
                << std::endl;
        }

        // render the channel name and severity
        buffer
            // start things off with the marker
            << palette[severity] << _footerMarker
            << palette["reset"]
            // the channel severity and name
            << "because the " << palette[severity] << severity << palette["reset"] << " channel '"
            << palette[severity] << channel << palette["reset"]
            << "' is active"
            // done with the intro line
            << std::endl;
    }

    // now for the extra notes, if any
    if (chronicler_t::decor() > 1) {
        // build a set of the keys we have processed already
        std::set<entry_type::key_type> known { "severity", "channel",  "filename",
                                               "line",     "function", "application" };
        // go through the notes
        for (auto & [key, value] : notes) {
            // if the key is in the known pile
            if (known.find(key) != known.end()) {
                // ignore it
                continue;
            }
            // otherwise, render it
            buffer << palette[severity] << _footerMarker << palette["reset"] << palette[severity]
                   << key << palette["reset"] << ": " << palette[severity] << value
                   << palette["reset"] << std::endl;
        }
    }

    // all done
    return;
}


// end of file
