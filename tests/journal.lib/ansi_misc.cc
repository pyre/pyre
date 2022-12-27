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


// verify that the colors in the misc color palette are registered correctly
int main() {

    // verify the contents of the {misc} color table
    assert ((ansi_t::misc("normal") == csi_t::reset()));
    assert ((ansi_t::misc("amber") == csi_t::csi24(0xff, 0xbf, 0x00)));

    // all done
    return 0;
}


// end of file
