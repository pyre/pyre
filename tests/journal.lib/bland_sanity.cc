// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>


// type aliases
using ansi_t = pyre::journal::ansi_t;
using bland_t = pyre::journal::bland_t;
using info_t = pyre::journal::info_t;
using chronicler_t = pyre::journal::chronicler_t;


// exercise the {bland} renderer
int
main()
{
    // grab the global metadata table from chronicler
    auto & globals = chronicler_t::notes();
    // set some metadata
    globals["application"] = "bland";
    globals["author"] = "michael";

    // use a channel to build a document and its metadata
    info_t channel("bland");
    // put some stuff in it; careful not to flush so we don't lose everything
    channel << pyre::journal::at(__HERE__) << pyre::journal::note("time", "now")
            << pyre::journal::note("device", "null") << "simon says:" << pyre::journal::newline
            << "hello world!" << pyre::journal::newline;

    // make a palette
    bland_t::palette_type palette;
    // add some decorations
    palette["reset"] = ansi_t::x11("normal");
    palette["channel"] = ansi_t::x11("light slate gray");
    palette["info"] = ansi_t::x11("steel blue");
    palette["body"] = "";

    // pull the entry
    auto & entry = channel.entry();
    // make a bland renderer
    bland_t bland;
    // ask it to render what we have
    bland.render(palette, entry);

    // all done
    return 0;
}


// end of file
