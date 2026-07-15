// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// what mpi reports about a message transfer that has completed
//
// this is the one mpi entity that is a plain struct rather than an opaque handle, so it needs
// no reference counting; it is copied by value, exactly as the c api intends
class pyre::mpi::Status {
    // types
public:
    // me
    using self_type = Status;
    // the struct the mpi c api fills in
    using raw_type = MPI_Status;

    // metamethods
public:
    // build an empty status, ready to be handed to a receive
    inline Status();
    // adopt a status that mpi has already filled in
    explicit inline Status(const raw_type & status);
    // the full set; a status is just data
    inline Status(const Status &) = default;
    inline Status(Status &&) noexcept = default;
    inline Status & operator=(const Status &) = default;
    inline Status & operator=(Status &&) noexcept = default;
    inline ~Status() = default;

    // interface
public:
    // the rank of the process that sent the message
    inline auto source() const -> rank_t;
    // the label the message carried
    inline auto tag() const -> tag_t;
    // whether the transfer itself failed
    inline auto error() const -> int;
    // whether the transfer was cancelled before it could complete
    inline auto cancelled() const -> bool;

    // how many cells of type {cellT} the message held
    template <typename cellT>
    inline auto count() const -> size_type;
    // the same, when the caller names the layout explicitly
    inline auto count(datatype_t type) const -> size_type;

    // the underlying struct, for handing to the mpi c api
    inline auto raw() -> raw_type *;
    inline auto raw() const -> const raw_type *;

    // data
private:
    // the struct mpi fills in
    raw_type _status;
};


// get the inline definitions
#include "Status.icc"


// end of file
