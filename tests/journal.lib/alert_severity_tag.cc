// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using alert_t = pyre::journal::alert_t;
using info_t = pyre::journal::info_t;
using chronicler_t = pyre::journal::chronicler_t;


// when no application name is registered, the alert header tags the message with the channel
// severity rather than the sentinel default
int
main()
{
    // reach the global metadata
    auto & globals = chronicler_t::notes();
    // leave the application unset, i.e. at the sentinel default the chronicler seeds
    globals["application"] = "journal";

    // use a channel whose name differs from its severity, so the tag and the channel name
    // cannot be confused
    info_t channel("tests.journal.flow");
    // put something on its page, since an empty page renders nothing
    channel << pyre::journal::at() << "hello world!" << pyre::journal::newline;

    // a palette with no color decorations, so the rendered text is the bare content
    alert_t::palette_type palette;
    // every lookup resolves to an empty string
    palette["reset"] = "";
    palette["info"] = "";
    palette["body"] = "";

    // pull the entry
    auto & entry = channel.entry();
    // render the message
    auto page = alert_t().render(palette, entry);
    // the header is the first line, of the form "{tag} ({channel}):"
    auto tag = page.substr(0, page.find(" "));
    // with no application registered, the tag is the severity
    assert(tag == "info");

    // all done
    return 0;
}


// end of file
