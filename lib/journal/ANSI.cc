// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// external support
#include "externals.h"
// get the forward declarations
#include "forward.h"
// and the type aliases
#include "api.h"
// get the support we need
#include "ASCII.h"
#include "CSI.h"
#include "ANSI.h"


// compatibility check
auto
pyre::journal::ANSI::
compatible() -> bool
{
    // get my instance
    const ANSI & instance = initialize();
    // and ask it
    return instance._compatible;
}


// access to the color tables
auto
pyre::journal::ANSI::
null(const name_type & color) -> csi_type
{
    // there's nothing ever in this table...
    return "";
}


auto
pyre::journal::ANSI::
ansi(const name_type & color) -> csi_type
{
    // get me my instance
    const ANSI & instance = initialize();
    // access the color table
    const table_type & table = instance._ansi;
    // try to look up the color name
    auto spot = table.find(color);
    // if not there, return an empty string; otherwise return the corresponding escape sequence
    return spot == table.end() ? "" : spot->second;
}


auto
pyre::journal::ANSI::
gray(const name_type & color) -> csi_type
{
    // get me my instance
    const ANSI & instance = initialize();
    // access the color table
    const table_type & table = instance._gray;
    // try to look up the color name
    auto spot = table.find(color);
    // if not there, return an empty string; otherwise return the corresponding escape sequence
    return spot == table.end() ? "" : spot->second;
}


auto
pyre::journal::ANSI::
x11(const name_type & color) -> csi_type
{
    // get me my instance
    const ANSI & instance = initialize();
    // access the color table
    const table_type & table = instance._x11;
    // try to look up the color name
    auto spot = table.find(color);
    // if not there, return an empty string; otherwise return the corresponding escape sequence
    return spot == table.end() ? "" : spot->second;
}


auto
pyre::journal::ANSI::
misc(const name_type & color) -> csi_type
{
    // get me my instance
    const ANSI & instance = initialize();
    // access the color table
    const table_type & table = instance._misc;
    // try to look up the color name
    auto spot = table.find(color);
    // if not there, return an empty string; otherwise return the corresponding escape sequence
    return spot == table.end() ? "" : spot->second;
}


// the singleton factory
auto
pyre::journal::ANSI::
initialize() -> const ANSI &
{
    // make one, once...
    static ANSI * ptr { new ANSI() };
    // and return it
    return *ptr;
}


// metamethods
pyre::journal::ANSI::
ANSI() :
    // copatibility flag
    _compatible { emulates() },
    // color tables
    _ansi { make_ansi() },
    _gray { make_gray() },
    _x11 { make_x11() },
    _misc { make_misc() }
{}


// implementations
auto
pyre::journal::ANSI::
emulates() -> bool
{
    // get the {TERM} environment variable
    auto term = std::getenv("TERM");
    // if the value is not set
    if (term == nullptr) {
        // we don't know, so better be safe
        return false;
    }

    // the set of compatible terminal types
    nameset_t compatible { "ansi",
                           "vt102", "vt220", "vt320", "vt420",
                           "xterm", "xterm-color", "xterm-16color", "xterm-256color" };

    // if the value is not in the set of supported emulations
    if (compatible.find(term) == compatible.end()) {
        // report failure
        return false;
    }

    // otherwise, all good
    return true;
}


auto
pyre::journal::ANSI::
make_ansi() -> table_type
{
    // make a table
    ansi_t::table_type table;

    // the reset sequence
    table["normal"] = csi_t::reset();

    // regular colors
    table["black"] = csi_t::csi3(30);
    table["red"] = csi_t::csi3(31);
    table["green"] = csi_t::csi3(32);
    table["brown"] = csi_t::csi3(33);
    table["blue"] = csi_t::csi3(34);
    table["purple"] = csi_t::csi3(35);
    table["cyan"] = csi_t::csi3(36);
    table["light-gray"] = csi_t::csi3(37);

    // bright colors
    table["dark-gray"] = csi_t::csi3(30, true);
    table["light-red"] = csi_t::csi3(31, true);
    table["light-green"] = csi_t::csi3(32, true);
    table["yellow"] = csi_t::csi3(33, true);
    table["light-blue"] = csi_t::csi3(34, true);
    table["light-purple"] = csi_t::csi3(35, true);
    table["light-cyan"] = csi_t::csi3(36, true);
    table["white"] = csi_t::csi3(37, true);

    // all done
    return table;
}


auto
pyre::journal::ANSI::
make_gray() -> table_type
{
    // make a table
    ansi_t::table_type table;

    // the reset sequence
    table["normal"] = csi_t::reset();

    // grays
    table["gray10"] = csi_t::csi24(0x19, 0x19, 0x19);
    table["gray30"] = csi_t::csi24(0x4c, 0x4c, 0x4c);
    table["gray41"] = csi_t::csi24(0x69, 0x69, 0x69);
    table["gray50"] = csi_t::csi24(0x80, 0x80, 0x80);
    table["gray66"] = csi_t::csi24(0xa9, 0xa9, 0xa9);
    table["gray75"] = csi_t::csi24(0xbe, 0xbe, 0xbe);

    // all done
    return table;
}


auto
pyre::journal::ANSI::
make_misc() -> table_type
{
    // make a table
    ansi_t::table_type table;

    // the reset sequence
    table["normal"] = csi_t::reset();

    // other custom colors
    table["amber"] = csi_t::csi24(0xff, 0xbf, 0x00);
    table["sage"] = csi_t::csi24(176, 208, 176);

    // all done
    return table;
}


// end of file
