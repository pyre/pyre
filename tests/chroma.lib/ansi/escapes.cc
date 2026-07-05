// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the chroma interface
#include <pyre/chroma.h>


// bring the color type into scope
using rgb_t = pyre::chroma::rgb_t;


// verify that the {ansi} serializers assemble the escape sequences we expect
int
main(int argc, char * argv[])
{
    // the reset sequence returns the terminal to its defaults
    assert(pyre::chroma::ansi::reset() == "\x1b[0m");

    // pure red as a 24-bit foreground scales to the full-byte red channel
    assert(pyre::chroma::ansi::rgb(rgb_t { 1, 0, 0 }) == "\x1b[38;2;255;0;0m");
    // pure white as a 24-bit background selects the background plane
    assert(pyre::chroma::ansi::rgb(rgb_t { 1, 1, 1 }, false) == "\x1b[48;2;255;255;255m");

    // black is the first cube index, 16
    assert(pyre::chroma::ansi::rgb256(rgb_t { 0, 0, 0 }) == "\x1b[38;5;16m");
    // white is the last cube index, 16 + 36·5 + 6·5 + 5 = 231
    assert(pyre::chroma::ansi::rgb256(rgb_t { 1, 1, 1 }) == "\x1b[38;5;231m");

    // the darkest gray is the bottom of the ramp, 232
    assert(pyre::chroma::ansi::gray(0) == "\x1b[38;5;232m");
    // the lightest gray is the top of the ramp, 255
    assert(pyre::chroma::ansi::gray(1) == "\x1b[38;5;255m");

    // a 16-color code renders with its weight and its code
    assert(pyre::chroma::ansi::csi3(30) == "\x1b[0;30m");
    assert(pyre::chroma::ansi::csi3(31, true) == "\x1b[1;31m");

    // all done
    return 0;
}


// end of file
