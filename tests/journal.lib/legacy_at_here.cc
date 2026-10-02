// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <string>


// the form is deprecated, and exercising it is the point of this test
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"


// an entry that starts with the deprecated {at(__HERE__)} records the location of the caller
int
main()
{
    // make a channel
    pyre::journal::info_t channel("tests.journal.legacy");
    // send its output to the trash
    channel.device<pyre::journal::trash_t>();

    // record the line of the entry
    const auto line = std::to_string(__LINE__ + 1);
    channel << pyre::journal::at(__HERE__) << "legacy" << pyre::journal::endl;

    // get the notes
    const auto & notes = channel.entry().notes();
    // the file is this one
    if (notes.at("filename") != __FILE__) {
        // indicate failure
        return 1;
    }
    // the line is that of the entry
    if (notes.at("line") != line) {
        // indicate failure
        return 1;
    }
    // and the function is this one, by its bare name
    if (notes.at("function") != __func__) {
        // indicate failure
        return 1;
    }

    // all done
    return 0;
}


// end of file
