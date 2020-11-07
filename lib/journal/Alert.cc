// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


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
pyre::journal::Alert::
~Alert()
{}


// implementation details
void
pyre::journal::Alert::
header(palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();
    // get the notes
    auto & notes = entry.notes();

    // if there is nothing to print
    if (page.empty()) {
        // we are done
        return;
    }

    // get the severity
    auto severity = notes.at("severity");
    // the reset sequence
    auto resetColor = palette["reset"];
    // ask the palette for the severity decoration
    auto severityColor = palette[severity];

    // print the application name and the severity in the correct color
    buffer
        << severityColor << notes.at("application") << resetColor
        << " "
        << severityColor << severity << resetColor
        << ": "
        << severityColor << notes.at("channel") << resetColor
        << ":"
        << std::endl;

    // all done
    return;
}


void
pyre::journal::Alert::
body(palette_type & palette, linebuf_type & buffer, const entry_type & entry) const
{
    // get the page
    auto & page = entry.page();
    // get the notes
    auto & notes = entry.notes();

    // if the page is empty
    if (page.empty()) {
        // do nothing
        return;
    }

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
        buffer
            << severityColor << " >> " << bodyColor << line << resetColor
            << std::endl;
    }

    // attempt to get location information
    // N.B.: we only print line number and function name if we know the filename
    auto loc = notes.find("filename");
    // if it's there
    if (loc != notes.end()) {
        // extract the filename
        auto filename = loc->second;
        // make some room and turn on location formatting
        buffer << severityColor << " >> " << resetColor;
        // set a maximum length for the rendered filename
        const line_type::size_type maxlen = 60;
        // get the filename size
        auto len = filename.size();
        // so that names that are longer than this maximum
        if (len > maxlen) {
            // get shortened
            buffer
                << filename.substr(0, maxlen/4 - 3)
                << "..."
                << filename.substr(len - 3*maxlen/4);
        } else {
            // otherwise, render the whole name
            buffer << filename;
        }
        // add a spacer
        buffer <<":";

        // attempt to get the line number
        auto & line = notes.at("line");
        // if we know it
        if (!line.empty()) {
            // render it
            buffer << line << ":";
        }

        // same with the function name
        auto & function = notes.at("function");
        // if we know it
        if (!function.empty()) {
            // render it
            buffer << function;
        }
        // wrap up the location info
        buffer << std::endl;
    }


    // all done
    return;
}


// end of file
