// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// add the bindings for an asynchronous message from another session
void
pyre::postgres::py::notification(py::module & m)
{
    // the class
    auto cls = py::class_<Notification>(
        // in scope
        m,
        // the name
        "Notification",
        // the docstring
        "a message a session collected from a channel it is listening to");

    // the channel it arrived on
    cls.def_readonly(
        // the name
        "channel",
        // the implementation
        &Notification::channel,
        // the docstring
        "the channel this message arrived on");

    // who sent it
    cls.def_readonly(
        // the name
        "backend",
        // the implementation
        &Notification::backend,
        // the docstring
        "the process id of the session that sent it");

    // and what they had to say
    cls.def_readonly(
        // the name
        "payload",
        // the implementation
        &Notification::payload,
        // the docstring
        "whatever that session had to say; the empty string when it said nothing");

    // for the benefit of anybody staring at a prompt
    cls.def(
        // the name
        "__repr__",
        // the implementation
        [](const Notification & self) -> string_t {
            return "<postgres.Notification on '" + self.channel + "' from "
                 + std::to_string(self.backend) + ">";
        },
        // the docstring
        "a human readable summary of this message");

    // all done
    return;
}


// end of file
