// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the recipe for releasing a session
struct pyre::postgres::ConnectionHandle {
    // types
public:
    // me
    using self_type = ConnectionHandle;
    // libpq hands out sessions as pointers to an opaque struct
    using handle_type = PGconn *;

    // metamethods
public:
    // the full set, so the copy and move behavior is never left to inference
    ConnectionHandle() = default;
    ConnectionHandle(const ConnectionHandle &) = default;
    ConnectionHandle(ConnectionHandle &&) noexcept = default;
    ConnectionHandle & operator=(const ConnectionHandle &) = default;
    ConnectionHandle & operator=(ConnectionHandle &&) noexcept = default;
    ~ConnectionHandle() = default;

    // interface
public:
    // hand {connection} back to libpq, and null it so that nobody tries again; never throws,
    // because this runs from a destructor
    static inline auto free(handle_type & connection) noexcept -> void;
};


// the recipe for releasing a result set
struct pyre::postgres::ResultHandle {
    // types
public:
    // me
    using self_type = ResultHandle;
    // as above, a pointer to an opaque struct
    using handle_type = PGresult *;

    // metamethods
public:
    // the full set, so the copy and move behavior is never left to inference
    ResultHandle() = default;
    ResultHandle(const ResultHandle &) = default;
    ResultHandle(ResultHandle &&) noexcept = default;
    ResultHandle & operator=(const ResultHandle &) = default;
    ResultHandle & operator=(ResultHandle &&) noexcept = default;
    ~ResultHandle() = default;

    // interface
public:
    // hand {result} back to libpq, and null it; never throws
    static inline auto free(handle_type & result) noexcept -> void;
};


// get the inline definitions
#include "traits.icc"


// end of file
