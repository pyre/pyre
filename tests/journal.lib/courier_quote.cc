// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>
#include <unistd.h>


// alias the types
using courier_t = pyre::journal::courier_t;
using chronicler_t = pyre::journal::chronicler_t;
using info_t = pyre::journal::info_t;


// text that needs escaping is rendered as JSON requires, and non-ascii text passes through
int
main()
{
    // make a pipe
    int pipes[2];
    assert(::pipe(pipes) == 0);
    // make a courier on its write end and install it
    auto courier = std::make_shared<courier_t>(pipes[1]);
    chronicler_t::device(courier);

    // an entry with awkward text in its page and its notes
    info_t channel("test.courier.quote");
    channel << pyre::journal::note("multi", "a\nb") << pyre::journal::note("odd", "\x01\x1f")
            << "quote \" backslash \\ tab \t bell \b feed \f return \r greek αβγ"
            << pyre::journal::endl;
    // it went out
    assert(courier->shipped() == 1);

    // read it
    char buffer[64 * 1024];
    auto got = ::read(pipes[0], buffer, sizeof(buffer));
    assert(got > 0);
    std::string line(buffer, got);
    // the page line, escaped
    assert(
        line.find(
            "\"page\":[\"quote \\\" backslash \\\\ tab \\t bell \\b feed \\f return \\r "
            "greek αβγ\"]")
        != std::string::npos);
    // the notes, escaped
    assert(line.find("\"multi\":\"a\\nb\"") != std::string::npos);
    assert(line.find("\"odd\":\"\\u0001\\u001f\"") != std::string::npos);
    // and still exactly one line
    assert(std::count(line.begin(), line.end(), '\n') == 1);

    // clean up
    courier->close();
    ::close(pipes[0]);

    // all done
    return 0;
}


// end of file
