// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>
#include <sstream>

// type aliases
using info_t = pyre::journal::info_t;
using splitter_t = pyre::journal::splitter_t;
using stream_t = pyre::journal::stream_t;


// verify that an entry sent to a splitter reaches every device attached to it
int
main()
{
    // two buffers
    std::ostringstream first, second;
    // a device over each
    auto one = std::make_shared<stream_t>("first", first);
    auto two = std::make_shared<stream_t>("second", second);
    // a splitter over both
    auto splitter = std::make_shared<splitter_t>(splitter_t::outputs_type { one, two });
    // make a channel
    info_t channel("tests.journal.splitter");
    // send its output to the splitter
    channel.device(splitter);
    // inject something
    channel << "hello world!" << pyre::journal::endl(__HERE__);
    // both buffers got the message
    assert(first.str().find("hello world!") != std::string::npos);
    assert(second.str().find("hello world!") != std::string::npos);
    // and the same message
    assert(first.str() == second.str());
    // all done
    return 0;
}


// end of file
