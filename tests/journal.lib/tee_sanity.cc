// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>
#include <fstream>

// type aliases
using info_t = pyre::journal::info_t;
using tee_t = pyre::journal::tee_t;


// verify that a tee writes to the console and to its files
int
main()
{
    // the file
    auto filename = tee_t::path_type("tee_sanity.log");
    // make a tee over the console and the file
    auto tee = std::make_shared<tee_t>(tee_t::paths_type { filename });
    // check its name
    assert(tee->name() == "tee");
    // it holds the console and the file
    assert(tee->outputs().size() == 2);
    // make a channel
    info_t channel("tests.journal.tee");
    // send its output to the tee
    channel.device(tee);
    // inject something; the console gets a copy, and so does the file
    channel << "hello world!" << pyre::journal::endl(__HERE__);
    // let go of the tee so the file is flushed and closed
    channel.device<pyre::journal::trash_t>();
    tee.reset();
    // read the file back
    std::ifstream log(filename);
    std::string text((std::istreambuf_iterator<char>(log)), std::istreambuf_iterator<char>());
    // and check that the message is there
    assert(text.find("hello world!") != std::string::npos);
    // all done
    return 0;
}


// end of file
