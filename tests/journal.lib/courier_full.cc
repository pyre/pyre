// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>
#include <cerrno>
#include <fcntl.h>
#include <unistd.h>


// alias the types
using courier_t = pyre::journal::courier_t;
using chronicler_t = pyre::journal::chronicler_t;
using info_t = pyre::journal::info_t;


// read everything a non-blocking descriptor has to offer right now
static auto
slurp(int descriptor) -> std::string
{
    // the pile
    std::string pile;
    // a chunk
    char buffer[64 * 1024];
    // for as long as there is something
    while (true) {
        // read a chunk
        auto got = ::read(descriptor, buffer, sizeof(buffer));
        // if the pipe is empty, or drained
        if (got <= 0) {
            // done
            break;
        }
        // accumulate
        pile.append(buffer, got);
    }
    // all done
    return pile;
}


// split a byte string into lines, reporting whether the last one was terminated
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
            // whatever is left is a partial line, which must not happen
            assert(start == data.size());
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


// pull a numeric note out of a record
static auto
field(const std::string & record, const std::string & key) -> long
{
    // find the key; notes are strings, so the number is quoted
    auto at = record.find(key);
    assert(at != std::string::npos);
    // and read the number that follows it
    return std::stol(record.substr(at + key.size()));
}


// a far end that does not keep up costs records, never time; the loss is counted and reported
int
main()
{
    // make a pipe; nobody reads it for a while
    int pipes[2];
    // the call must happen whether or not assertions are compiled in, so check it by hand
    if (::pipe(pipes) != 0) {
        // no pipe, no test
        return 1;
    }
    // make a courier on its write end and install it
    auto courier = std::make_shared<courier_t>(pipes[1]);
    chronicler_t::device(courier);

    // a line long enough to fill any pipe buffer in a few hundred entries
    std::string filler(1024, 'x');
    // the number of entries to attempt
    const size_t attempts = 1024;
    // log them all without reading; each call must return, whatever the state of the pipe
    for (size_t i = 0; i < attempts; ++i) {
        info_t channel("test.courier.full");
        channel << filler << pyre::journal::endl;
    }
    // every attempt was stamped, and so was every report of drops that found room to go out
    // between refusals, so the sequence runs at least as far as the attempts
    assert(courier->seq() >= attempts);
    // some were lost
    assert(courier->dropped() > 0);

    // drain the pipe; the read end must not block either
    ::fcntl(pipes[0], F_SETFL, ::fcntl(pipes[0], F_GETFL, 0) | O_NONBLOCK);
    auto received = slurp(pipes[0]);
    // log once more; the far end has caught up, so this one goes out, preceded by the report
    info_t after("test.courier.full");
    after << "after" << pyre::journal::endl;
    // the drops were reported
    assert(courier->dropped() == 0);
    // read the rest
    received += slurp(pipes[0]);

    // split into records; every line is whole, since records are never torn
    auto records = lines(received);
    assert(records.size() >= 2);
    // the last two are the report and the entry that prompted it
    const auto & notice = records[records.size() - 2];
    const auto & last = records[records.size() - 1];
    // the report is on the courier's own channel
    assert(notice.find("\"channel\":\"journal.courier\"") != std::string::npos);
    assert(notice.find("\"severity\":\"warning\"") != std::string::npos);
    // and the entry that prompted it follows
    assert(last.find("\"page\":[\"after\"]") != std::string::npos);
    // go through the records
    long previous = 0;
    long reported = 0;
    long notices = 0;
    for (const auto & record : records) {
        // the sequence numbers are increasing
        auto seq = field(record, "\"seq\":\"");
        assert(seq > previous);
        previous = seq;
        // a report of drops carries its count in its notes
        if (record.find("\"channel\":\"journal.courier\"") != std::string::npos) {
            // every report accounts for at least one loss
            auto dropped = field(record, "\"dropped\":\"");
            assert(dropped > 0);
            // tally
            reported += dropped;
            ++notices;
        }
    }
    // the entries that made it out are the records that are not reports
    assert(static_cast<long>(courier->shipped()) == static_cast<long>(records.size()) - notices);
    // every attempt, the final entry included, was either shipped or reported lost
    assert(static_cast<long>(courier->shipped()) + reported == static_cast<long>(attempts) + 1);
    // and the gaps in the sequence account for exactly the losses
    assert(previous - static_cast<long>(records.size()) == reported);

    // clean up
    courier->close();
    ::close(pipes[0]);

    // all done
    return 0;
}


// end of file
