// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using csi_t = pyre::journal::csi_t;
using ansi_t = pyre::journal::ansi_t;


// verify that the gray tones are registered correctly
int main() {

    // verify the contents of the {gray} color table
    assert ((ansi_t::gray("normal") == csi_t::reset()));
    assert ((ansi_t::gray("gray10") == csi_t::csi24(0x19, 0x19, 0x19)));
    assert ((ansi_t::gray("gray30") == csi_t::csi24(0x4c, 0x4c, 0x4c)));
    assert ((ansi_t::gray("gray41") == csi_t::csi24(0x69, 0x69, 0x69)));
    assert ((ansi_t::gray("gray50") == csi_t::csi24(0x80, 0x80, 0x80)));
    assert ((ansi_t::gray("gray66") == csi_t::csi24(0xa9, 0xa9, 0xa9)));
    assert ((ansi_t::gray("gray75") == csi_t::csi24(0xbe, 0xbe, 0xbe)));

    // all done
    return 0;
}


// end of file
