// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// color encodings
// - pyre::journal::csi3(code, bright)
// - pyre::journal::csi8(red, green, blue, foreground);
// - pyre::journal::csi8_gray(gray, foreground);
// - pyre::journal::csi24(red, green, blue, foreground)
// color tables
// - pyre::journal::ansi
// - pyre::journal::x11


// exercise a few channel color manipulators
int
main()
{
    // make a debug channel
    pyre::journal::debug_t channel("tests.journal.debug");

    // activate it
    channel.activate();
    // but send the output to the trash
    channel.device<pyre::journal::trash_t>();

    // inject something into the channel
    channel
        // pick a color from one of the supported color tables
        << pyre::journal::x11("purple")
        // and say something
        << "hello"
        // reset the color to whatever it was before
        << pyre::journal::ansi("normal")
        // and say something more
        << " in "
        // use an explicit color sequence
        << pyre::journal::csi24(0xff, 0xbf, 0x00)
        // to colorize a word
        << "color"
        // reset the color to whatever it was before
        << pyre::journal::ansi("normal")
        // and flush
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file
