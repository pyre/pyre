// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the engine that reaches the cells of grids on host storage
class pyre::py::grid::HostEngine {
    // types
public:
    // me
    using self_type = HostEngine;

    // interface
public:
    // make the cells within reach of the host; they always are
    static auto access() -> void;

    // metamethods
public:
    // an engine is a collection of static functions, so there are no instances
    HostEngine() = delete;
    // destructor
    ~HostEngine() = delete;
    // copy and move
    HostEngine(const HostEngine &) = delete;
    HostEngine(HostEngine &&) = delete;
    HostEngine & operator=(const HostEngine &) = delete;
    HostEngine & operator=(HostEngine &&) = delete;
};


// end of file
