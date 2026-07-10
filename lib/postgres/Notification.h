// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// an asynchronous message from another session
//
// a session that has said {LISTEN} on some channel collects one of these every time any session,
// including itself, says {NOTIFY} on it. postgres delivers them alongside the answers to
// ordinary statements, so they are picked up by asking, rather than by being interrupted
struct pyre::postgres::Notification {
    // types
public:
    using string_type = string_t;

    // metamethods
public:
    // assemble a message
    inline Notification(string_type channel, int backend, string_type payload);
    // the full set, so the copy and move behavior is never left to inference
    inline Notification(const Notification &) = default;
    inline Notification(Notification &&) noexcept = default;
    inline Notification & operator=(const Notification &) = default;
    inline Notification & operator=(Notification &&) noexcept = default;
    inline ~Notification() = default;

    // data
public:
    // the channel it arrived on
    string_type channel;
    // the process id of the session that sent it
    int backend;
    // whatever that session had to say, which is the empty string when it said nothing
    string_type payload;
};


// get the inline definitions
#include "Notification.icc"


// end of file
