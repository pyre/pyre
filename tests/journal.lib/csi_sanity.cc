// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using ascii_t = pyre::journal::ascii_t;
using csi_t = pyre::journal::csi_t;


// verify we can build escape sequences correctly
int main() {
    // setup {ESC} so we don't have interpretable command sequences in the code
    csi_t::rep_type ESC { ascii_t::ESC };

    // verify the escape sequence generation routines build the correct strings
    assert ((csi_t::csi3(35) == ESC + "[0;35m"));
    assert ((csi_t::csi8(4,2,3) == ESC + "[38;5;175m"));
    assert ((csi_t::csi8_gray(16) == ESC + "[38;5;248m"));
    assert ((csi_t::csi24(0xff, 0xbf, 0x00) == ESC + "[38;2;255;191;0m"));

    // all done
    return 0;
}


// end of file
