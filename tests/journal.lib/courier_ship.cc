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


// split a byte string into lines
static auto
lines(const std::string & data) -> std::vector<std::string>
{
    // the pile
    std::vector<std::string> pile;
    // the start of the current line
    std::string::size_type start = 0;
    // for as long as there are newlines
    while (true) {
        // find the next one
        auto end = data.find('\n', start);
        // if there isn't one
        if (end == std::string::npos) {
            // done
            break;
        }
        // save the line
        pile.push_back(data.substr(start, end - start));
        // and move past it
        start = end + 1;
    }
    // all done
    return pile;
}


// every severity reaches the courier through the right sink, in order, with its page intact
int
main()
{
    // make a pipe
    int pipes[2];
    assert(::pipe(pipes) == 0);
    // make a courier on its write end and install it
    auto courier = std::make_shared<courier_t>(pipes[1]);
    chronicler_t::device(courier);

    // the channel name
    std::string name("test.courier.ship");
    // a two line entry with some indentation, through each of the quiet severities
    {
        pyre::journal::info_t channel(name);
        channel << "first" << pyre::journal::newline << pyre::journal::indent << "second"
                << pyre::journal::newline << pyre::journal::outdent << "third"
                << pyre::journal::endl;
    }
    {
        pyre::journal::warning_t channel(name);
        channel << "first" << pyre::journal::newline << pyre::journal::indent << "second"
                << pyre::journal::newline << pyre::journal::outdent << "third"
                << pyre::journal::endl;
    }
    {
        pyre::journal::help_t channel(name);
        channel << "first" << pyre::journal::newline << pyre::journal::indent << "second"
                << pyre::journal::newline << pyre::journal::outdent << "third"
                << pyre::journal::endl;
    }
    {
        pyre::journal::debug_t channel(name);
        // debug channels are off by default
        channel.activate();
        channel << "first" << pyre::journal::newline << pyre::journal::indent << "second"
                << pyre::journal::newline << pyre::journal::outdent << "third"
                << pyre::journal::endl;
    }
    // the fatal severities raise after delivering
    try {
        pyre::journal::error_t channel(name);
        channel << "boom" << pyre::journal::endl;
        // unreachable
        assert(false);
    } catch (const pyre::journal::application_error &) {
        // as expected
    }
    try {
        pyre::journal::firewall_t channel(name);
        channel << "boom" << pyre::journal::endl;
        // unreachable
        assert(false);
    } catch (const pyre::journal::firewall_error &) {
        // as expected
    }

    // every entry made it out
    assert(courier->seq() == 6);
    assert(courier->shipped() == 6);
    assert(courier->dropped() == 0);

    // read the records back
    char buffer[64 * 1024];
    auto got = ::read(pipes[0], buffer, sizeof(buffer));
    assert(got > 0);
    auto records = lines(std::string(buffer, got));
    // one per entry
    assert(records.size() == 6);

    // the sink and severity each one should carry
    const char * sinks[] = { "alert", "alert", "help", "memo", "alert", "memo" };
    const char * severities[] = { "info", "warning", "help", "debug", "error", "firewall" };
    // go through them
    for (size_t i = 0; i < records.size(); ++i) {
        // the record
        const auto & record = records[i];
        // the sequence numbers are consecutive
        assert(record.find("\"seq\":" + std::to_string(i + 1) + ",") != std::string::npos);
        // the sink is right
        assert(record.find(std::string("\"sink\":\"") + sinks[i] + "\"") != std::string::npos);
        // from the right channel
        assert(record.find("\"channel\":\"" + name + "\"") != std::string::npos);
        assert(
            record.find(std::string("\"severity\":\"") + severities[i] + "\"")
            != std::string::npos);
    }
    // the quiet ones carry the page as logged, indentation included
    for (size_t i = 0; i < 4; ++i) {
        assert(records[i].find("\"page\":[\"first\",\"  second\",\"third\"]") != std::string::npos);
    }
    // and the fatal ones carry theirs
    for (size_t i = 4; i < 6; ++i) {
        assert(records[i].find("\"page\":[\"boom\"]") != std::string::npos);
    }

    // clean up
    courier->close();
    ::close(pipes[0]);

    // all done
    return 0;
}


// end of file
