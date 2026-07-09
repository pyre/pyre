// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// what i report when my transfer completes
#include "Status.h"


// the receipt of a message transfer that is still in flight
//
// unlike a communicator or a group, a request is not a shareable thing: exactly one owner is
// entitled to complete it, and completing it twice is an error. so this one is move only, and
// owns its handle outright
class pyre::mpi::Request {
    // types
public:
    // the opaque token mpi uses to name a pending transfer
    using handle_type = MPI_Request;

    // metamethods
public:
    // build a request that names no transfer
    inline Request();
    // adopt a transfer that mpi has already started
    explicit inline Request(handle_type handle);
    // sharing a request would let two owners complete it, so refuse to copy
    Request(const Request &) = delete;
    Request & operator=(const Request &) = delete;
    // moving hands sole ownership along, leaving the source naming nothing
    inline Request(Request && other) noexcept;
    inline Request & operator=(Request && other) noexcept;
    // abandon whatever is still in flight
    inline ~Request();

    // interface
public:
    // the raw token, for handing to the mpi c api
    inline auto handle() const -> handle_type;
    // whether i still name a transfer that has not completed
    inline auto active() const -> bool;
    // contextual conversion to {bool}, true when i am {active}
    explicit inline operator bool() const;

    // block until my transfer completes, and report on it
    inline auto wait() -> Status;
    // check whether my transfer has completed, without blocking
    inline auto test() -> std::optional<Status>;
    // ask mpi to abandon my transfer
    inline auto cancel() -> void;
    // surrender my token to the caller, leaving me naming nothing; the caller now owes mpi
    // whatever completion the transfer still requires
    inline auto release() -> handle_type;

    // implementation details
private:
    // hand my token back to mpi, if i still hold one; never throws, because this runs from a
    // destructor and from the move assignment that precedes one
    inline auto _abandon() noexcept -> void;

    // data
private:
    // the token i own outright
    handle_type _request;
};


// waiting on many transfers at once
namespace pyre::mpi {
    // block until every one of {requests} completes, and report on each
    inline auto waitAll(std::vector<Request> & requests) -> std::vector<Status>;
} // namespace pyre::mpi


// get the inline definitions
#include "Request.icc"


// end of file
