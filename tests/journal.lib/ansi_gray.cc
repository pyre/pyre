// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using csi_t = pyre::journal::csi_t;
using ansi_t = pyre::journal::ansi_t;


// verify that the gray tones are registered correctly
int
main()
{
    // verify the contents of the {gray} color table; these are the canonical X11 gray values
    assert((ansi_t::gray("normal") == csi_t::reset()));
    assert((ansi_t::gray("gray10") == csi_t::csi24(0x1a, 0x1a, 0x1a)));
    assert((ansi_t::gray("gray30") == csi_t::csi24(0x4d, 0x4d, 0x4d)));
    assert((ansi_t::gray("gray41") == csi_t::csi24(0x69, 0x69, 0x69)));
    assert((ansi_t::gray("gray50") == csi_t::csi24(0x7f, 0x7f, 0x7f)));
    assert((ansi_t::gray("gray66") == csi_t::csi24(0xa8, 0xa8, 0xa8)));
    assert((ansi_t::gray("gray75") == csi_t::csi24(0xbf, 0xbf, 0xbf)));

    // all done
    return 0;
}


// end of file
