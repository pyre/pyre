// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the color palette; it is an opt-in header, not part of {pyre/chroma.h}
#include <pyre/chroma/rgb/palette.h>


// bring the color type into scope
using rgb_t = pyre::chroma::rgb_t;


// verify that the palette resolves canonical names to their exact triplets
int
main(int argc, char * argv[])
{
    // the achromatic extremes
    assert((pyre::chroma::rgb::palette::find("black") == rgb_t { 0, 0, 0 }));
    assert((pyre::chroma::rgb::palette::find("white") == rgb_t { 1, 1, 1 }));

    // the primaries, each of which wins its triplet over later aliases
    assert((pyre::chroma::rgb::palette::find("red") == rgb_t { 1, 0, 0 }));
    assert((pyre::chroma::rgb::palette::find("green") == rgb_t { 0, 1, 0 }));
    assert((pyre::chroma::rgb::palette::find("blue") == rgb_t { 0, 0, 1 }));

    // alias spellings and pyre's own colors resolve too — the palette is complete, not deduped
    assert(pyre::chroma::rgb::palette::find("fuchsia"));
    assert(pyre::chroma::rgb::palette::find("amber"));
    assert(pyre::chroma::rgb::palette::find("sage"));

    // a name that is not in the table reports a miss
    assert(!pyre::chroma::rgb::palette::find("not-a-color"));

    // all done
    return 0;
}


// end of file
