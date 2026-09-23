// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// the declarations
#include "diagnostics.h"
// stdlib
#include <string>


// the innermost frame of the error stack, captured while the library walks it
namespace pyre::h5 {
    // the walk visits every frame; the last one it sees from the bottom up is the innermost,
    // which names the routine that first refused and why
    static auto innermost(unsigned n, const H5E_error2_t * frame, void * client) -> herr_t
    {
        // the string the caller wants filled
        auto & text = *static_cast<std::string *>(client);
        // the frame's routine and its description
        std::string routine = frame->func_name ? frame->func_name : "";
        std::string reason = frame->desc ? frame->desc : "";
        // the innermost frame is visited last, so each visit replaces the previous answer
        text = routine.empty() ? reason : routine + ": " + reason;
        // keep walking
        return 0;
    }
} // namespace pyre::h5


// the library's explanation of its latest refusal
auto
pyre::h5::explanation() -> std::string
{
    // the answer
    std::string text;
    // walk the default error stack from the outermost frame down; a stack that will not be
    // walked, e.g. before the library is initialized, leaves the answer empty
    if (H5Ewalk2(H5E_DEFAULT, H5E_WALK_DOWNWARD, innermost, &text) < 0) {
        // so there is nothing to say
        return "";
    }
    // hand off whatever the innermost frame said
    return text;
}


// report a refusal
void
pyre::h5::complain(
    const char * channel, const std::string & attempt, const std::source_location location)
{
    // get the library's side of the story, before anything else disturbs it
    auto reason = explanation();
    // and report
    complain(channel, attempt, reason, location);
    // all done
    return;
}


// report a refusal whose explanation the caller collected
void
pyre::h5::complain(
    const char * channel, const std::string & attempt, const std::string & reason,
    const std::source_location location)
{
    // make a channel
    auto chn = pyre::journal::error_t(channel);
    // complain
    chn
        // where
        << pyre::journal::at(location)
        // what
        << "while " << attempt << ": the hdf5 library refused"
        << pyre::journal::newline
        // why, if the library said
        << pyre::journal::indent << (reason.empty() ? "no explanation on the error stack" : reason)
        << pyre::journal::outdent
        // flush
        << pyre::journal::endl;
    // all done
    return;
}


// end of file
