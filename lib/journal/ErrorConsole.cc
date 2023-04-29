// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// external support
#include "externals.h"
// get the forward declarations
#include "forward.h"
// type aliases
#include "api.h"

// global settings
#include "Chronicler.h"
// message contents
#include "Entry.h"

// support for color
#include "ASCII.h"
#include "CSI.h"
#include "ANSI.h"
// renderer support
#include "Renderer.h"
#include "Alert.h"
#include "Bland.h"
#include "Memo.h"
// the device declarations
#include "Device.h"
#include "Stream.h"
#include "ErrorConsole.h"

// access {std::cerr}
#include <iostream>
// get {isatty}
#include <unistd.h>


// metamethods
// constructor
pyre::journal::ErrorConsole::ErrorConsole() : Stream("cerr", std::cerr), _tty(isatty(2) == 1)
{
    // if i am connected to a compatible terminal
    if (_tty && ansi_t::compatible()) {
        // populate my palette with some colors
        // put things back to normal
        _palette["reset"] = ansi_t::x11("normal");
        // channel name
        _palette["channel"] = ansi_t::x11("purple");
        // severity
        _palette["info"] = ansi_t::x11("forest green");
        _palette["warning"] = ansi_t::x11("orange");
        _palette["error"] = ansi_t::x11("red");
        _palette["help"] = ansi_t::x11("cyan");
        _palette["debug"] = ansi_t::x11("cornflower blue");
        _palette["firewall"] = ansi_t::x11("fuchsia");
        // the page body
        _palette["body"] = ansi_t::x11("normal");
    }
}


// destructor
pyre::journal::ErrorConsole::~ErrorConsole() {}


// end of file
