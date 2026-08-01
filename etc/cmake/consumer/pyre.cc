// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the version, which is where the library and its headers can disagree
#include <pyre/version.h>
// and the journal, which we never link against explicitly; it has to arrive through {pyre::pyre}
#include <pyre/journal.h>


// verify that a client that knows nothing but {pyre::pyre} gets a working library: the headers
// where the exported target says they are, the symbols of {libpyre} at load time, {libjournal}
// pulled in transitively, and headers that match the library installed alongside them
int
main()
{
    // ask the library what it was built as
    const auto library = pyre::version::version();
    // and ask the headers what they describe
    const auto headers = pyre::version::headerVersion();

    // a mismatch means the prefix has a stale library or stale headers
    if (library != headers) {
        // so complain
        auto channel = pyre::journal::error_t("pyre.consumer.version");
        // with the two versions side by side
        channel
            // what
            << "the installed library and headers disagree about the version"
            << pyre::journal::newline
            // the details
            << "library: " << std::get<0>(library) << "." << std::get<1>(library) << "."
            << std::get<2>(library) << "." << std::get<3>(library) << pyre::journal::newline
            << "headers: " << std::get<0>(headers) << "." << std::get<1>(headers) << "."
            << std::get<2>(headers) << "." << std::get<3>(headers)
            // where
            << pyre::journal::endl(__HERE__);
        // and fail
        return 1;
    }

    // all done
    return 0;
}


// end of file
