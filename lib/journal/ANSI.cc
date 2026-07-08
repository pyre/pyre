// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external support
#include "externals.h"
// get the forward declarations
#include "forward.h"
// and the type aliases
#include "api.h"
// get the support we need
#include "ANSI.h"
// the single source of color truth, and its color-name palette
#include <pyre/chroma.h>
#include <pyre/chroma/rgb/palette.h>


// render a named color as a 24-bit escape sequence via {chroma}; {normal} means reset
static auto
named(const pyre::journal::ANSI::name_type & color) -> pyre::journal::ANSI::csi_type
{
    // {normal} restores the terminal defaults rather than naming a color
    if (color == "normal") {
        // so hand back the reset sequence
        return pyre::chroma::ansi::reset();
    }
    // otherwise look the name up in chroma's color palette
    auto found = pyre::chroma::rgb::palette::find(color);
    // an unknown name produces no color
    if (!found) {
        // i.e. an empty sequence
        return "";
    }
    // a known name renders as a 24-bit truecolor escape
    return pyre::chroma::ansi::rgb(*found);
}


// compatibility check
auto
pyre::journal::ANSI::compatible() -> bool
{
    // ask whether the current terminal emulates a compatible type
    return emulates();
}


// the null colorspace, where every color maps to an empty string
auto
pyre::journal::ANSI::null(const name_type & color) -> csi_type
{
    // there is never anything in this table
    return "";
}


// the sixteen named terminal colors, rendered through chroma's {csi3}
auto
pyre::journal::ANSI::ansi(const name_type & color) -> csi_type
{
    // {normal} restores the terminal defaults
    if (color == "normal") {
        // so hand back the reset sequence
        return pyre::chroma::ansi::reset();
    }

    // the names map to terminal palette codes, with the light variants marked {bright}
    static const std::map<name_type, std::pair<int, bool>> codes {
        { "black", { 30, false } },      { "red", { 31, false } },
        { "green", { 32, false } },      { "brown", { 33, false } },
        { "blue", { 34, false } },       { "purple", { 35, false } },
        { "cyan", { 36, false } },       { "light-gray", { 37, false } },
        { "dark-gray", { 30, true } },   { "light-red", { 31, true } },
        { "light-green", { 32, true } }, { "yellow", { 33, true } },
        { "light-blue", { 34, true } },  { "light-purple", { 35, true } },
        { "light-cyan", { 36, true } },  { "white", { 37, true } },
    };

    // look up the requested name
    auto spot = codes.find(color);
    // an unknown name produces no color
    if (spot == codes.end()) {
        // i.e. an empty sequence
        return "";
    }
    // render the code through chroma
    return pyre::chroma::ansi::csi3(spot->second.first, spot->second.second);
}


// the grays are ordinary named colors in the palette
auto
pyre::journal::ANSI::gray(const name_type & color) -> csi_type
{
    // so resolve them the same way
    return named(color);
}


// the X11 named colors live in the palette
auto
pyre::journal::ANSI::x11(const name_type & color) -> csi_type
{
    // so resolve them there
    return named(color);
}


// pyre's custom colors also live in the palette
auto
pyre::journal::ANSI::misc(const name_type & color) -> csi_type
{
    // so resolve them there too
    return named(color);
}


// the emulation check
auto
pyre::journal::ANSI::emulates() -> bool
{
    // get the {TERM} environment variable
    auto term = std::getenv("TERM");
    // if the value is not set
    if (term == nullptr) {
        // we don't know, so better be safe
        return false;
    }

    // the set of compatible terminal types
    nameset_t compatible { "ansi",  "vt102",       "vt220",         "vt320",         "vt420",
                           "xterm", "xterm-color", "xterm-16color", "xterm-256color" };

    // if the value is not in the set of supported emulations
    if (compatible.find(term) == compatible.end()) {
        // report failure
        return false;
    }

    // otherwise, all good
    return true;
}


// end of file
