// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved


#include <cassert>
#include <string>

#include <pyre/error.h>
#include <pyre/journal.h>


// check source location file name and line number
int
main(int argc, char * argv [])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("source_location");
    // make a channel
    pyre::journal::debug_t channel("pyre.error.source_location");

    // get current source location
    const auto location = pyre::error::source_location_t::current();

    // show me
    channel
        // show me the file name
        << "location.file_name() = " << location.file_name()
        << pyre::journal::newline
        // show me the line number
        << "location.line() = " << location.line() << pyre::journal::endl(__HERE__);

    // checks if a string ends with the given suffix
    auto ends_with = [](const std::string & str, const std::string & suffix) {
        const auto n = str.length();
        const auto m = suffix.length();
        if (n < m) {
            return false;
        }
        return str.compare(n - m, m, suffix) == 0;
    };

    // check file name
    assert(ends_with(location.file_name(), "source_location.cc"));
    // check line number
    assert(location.line() == 25);

    // all done
    return 0;
}


// end of file
