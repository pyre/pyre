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


// a courier installed on the chronicler ships an entry as a record down its descriptor
int
main()
{
    // make a pipe
    int pipes[2];
    assert(::pipe(pipes) == 0);
    // make a courier on its write end
    auto courier = std::make_shared<courier_t>(pipes[1]);
    // check its name
    assert(courier->name() == "courier");
    // and its initial state
    assert(courier->descriptor() == pipes[1]);
    assert(courier->seq() == 0);
    assert(courier->shipped() == 0);
    assert(courier->dropped() == 0);
    assert(!courier->dead());
    assert(!courier->mirror());

    // make it the default device
    chronicler_t::device(courier);
    // check the assignment sticks
    assert(chronicler_t::device() == courier);

    // make a channel and log something
    info_t channel("test.courier");
    channel << pyre::journal::at(__HERE__) << "hello world" << pyre::journal::endl;

    // the record made it out
    assert(courier->seq() == 1);
    assert(courier->shipped() == 1);
    assert(courier->dropped() == 0);
    // read it
    char buffer[64 * 1024];
    auto got = ::read(pipes[0], buffer, sizeof(buffer));
    assert(got > 0);
    // exactly one line
    std::string line(buffer, got);
    assert(line.back() == '\n');
    assert(std::count(line.begin(), line.end(), '\n') == 1);
    // with the version and the page first
    assert(line.find("{\"journal\":1,\"page\":[\"hello world\"]") == 0);
    // and the origin in the notes
    assert(line.find("\"pid\":\"" + std::to_string(::getpid()) + "\"") != std::string::npos);
    assert(line.find("\"seq\":\"1\"") != std::string::npos);
    assert(line.find("\"time\":\"") != std::string::npos);
    assert(line.find("\"host\":\"") != std::string::npos);
    // and the notes
    assert(line.find("\"channel\":\"test.courier\"") != std::string::npos);
    assert(line.find("\"severity\":\"info\"") != std::string::npos);
    assert(line.find("\"filename\":\"") != std::string::npos);
    assert(line.find("\"function\":\"main\"") != std::string::npos);
    // the record is an object
    assert(line.substr(line.size() - 3) == "}}\n");

    // closing releases the descriptor
    courier->close();
    assert(courier->dead());
    // so the reader sees the end of the stream
    assert(::read(pipes[0], buffer, sizeof(buffer)) == 0);
    // and closing again is harmless
    courier->close();
    // clean up
    ::close(pipes[0]);

    // all done
    return 0;
}


// end of file
