// -*- c++ -*-
//
// the pyre authors
// (c) 1998-2023 all rights reserved

#include <pyre/journal.h>
#include <cassert>
#include <sstream>

using pyre::journal::device_t;
using pyre::journal::splitter_t;
using pyre::journal::stream_t;
using logger_t = pyre::journal::info_t;

// split a log to multiple stringstreams
int main() {

    // helper
    auto contains = [](const std::string & s, const std::string & substr) {
        return s.find(substr) != s.npos;
    };

    // make outputs for splitter
    std::stringstream ss_a;
    std::stringstream ss_b;
    std::vector<std::shared_ptr<device_t>> devices {
        std::make_shared<stream_t>("Stream A", ss_a),
        std::make_shared<stream_t>("Stream B", ss_b)
    };

    // make channel
    logger_t logger("logger");
    logger.device<splitter_t>(devices);

    std::string magic = "journal is cool!";

    // just to be sure
    assert(not contains(ss_a.str(), magic));
    assert(not contains(ss_b.str(), magic));

    // log some magic
    logger << magic << pyre::journal::endl;

    // did the magic come out both ends of the splitter?
    assert(contains(ss_a.str(), magic));
    assert(contains(ss_b.str(), magic));
}

// end of file
