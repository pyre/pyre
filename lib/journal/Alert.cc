// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


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
#include "Alert.h"


// metamethods
pyre::journal::Alert::~Alert() {}


// implementation details
void
pyre::journal::Alert::header(
    palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();
    // if there is nothing to print
    if (page.empty()) {
        // we are done
        return;
    }

    // otherwise, get the notes
    auto & notes = entry.notes();
    // get the severity
    auto severity = notes.at("severity");
    // and the channel name
    auto channel = notes.at("channel");
    // ask the palette for the severity decoration
    auto severityColor = palette[severity];
    // and get the reset sequence
    auto resetColor = palette["reset"];

    // try to lookup the application name
    auto cursor = notes.find("application");
    // if it's there, use it; otherwise use the {severity}
    auto tag = (cursor != notes.end()) ? cursor->second : severity;
    // inject the tag, along with a space
    buffer << severityColor << tag << resetColor << " ";
    // followed by the channel name
    buffer << '(' << severityColor << channel << resetColor << "):" << std::endl;

    // all done
    return;
}


void
pyre::journal::Alert::body(
    palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();
    // if the page is empty
    if (page.empty()) {
        // do nothing
        return;
    }

    // otherwise, get the notes
    auto & notes = entry.notes();
    // get the severity
    auto severity = notes.at("severity");
    // the reset sequence
    auto resetColor = palette["reset"];
    // ask the palette for the severity decoration
    auto severityColor = palette[severity];
    // and the body color
    auto bodyColor = palette["body"];

    // go through the lines in the page
    for (auto line : page) {
        // and render each one
        buffer << severityColor << _bodyMarker << bodyColor << line << resetColor << std::endl;
    }

    return;
}


void
pyre::journal::Alert::footer(
    palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();
    // if there is nothing to print
    if (page.empty()) {
        // we are done
        return;
    }
    // get the notes
    auto & notes = entry.notes();
    // get the severity
    auto severity = notes.at("severity");
    // and the channel name
    auto channel = notes.at("channel");
    // the reset sequence
    auto resetColor = palette["reset"];
    // ask the palette for the severity decoration
    auto severityColor = palette[severity];

    // at the right decoration level
    if (chronicler_t::decor() > 1) {
        // attempt to get location information
        auto loc = notes.find("filename");
        // if it's there
        if (loc != notes.end()) {
            // extract the filename
            auto filename = loc->second;
            // make some room and turn on location formatting
            buffer << severityColor << _footerMarker << resetColor << "from ";
            // set a maximum length for the rendered filename
            const line_type::size_type maxlen = 80;
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
            // add a spacer
            buffer << ":";

            // attempt to get the line number
            auto & line = notes.at("line");
            // if we know it
            if (!line.empty()) {
                // render it
                buffer << line << ":";
            }
            // save this much
            buffer << std::endl;

            // get the function name
            auto & function = notes.at("function");
            // if we know it
            if (!function.empty()) {
                // render
                buffer
                    // make some room and turn on location formatting
                    << severityColor << _footerMarker
                    << resetColor
                    // the intro
                    << "in '"
                    // the function name
                    << function
                    // terminate and flush
                    << "'" << std::endl;
            }
        }
    }

    // at the right decoration level
    if (chronicler_t::decor() > 2) {
        // render the channel name and severity
        buffer
            // start things off with the marker
            << severityColor << _footerMarker
            << resetColor
            // the channel severity and name
            << "because the " << severityColor << severity << resetColor << " channel '"
            << severityColor << channel << resetColor
            << "' is active"
            // and done
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
            buffer
                // the marker
                << severityColor << _footerMarker
                << resetColor
                // the key
                << severityColor << key << resetColor
                << ": "
                // the value
                << severityColor << value << resetColor << std::endl;
        }
    }

    // all done
    return;
}


// end of file
