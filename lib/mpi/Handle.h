// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the shared owner of an mpi object handle
//
// mpi, unlike hdf5, keeps no reference count of its own for the objects it hands out, so we
// supply one. the count lives in a {std::shared_ptr}, which makes it atomic, makes copies and
// moves free, and makes the release path exception safe: the last owner to go away is the one
// that hands the handle back to mpi
template <class traitsT>
class pyre::mpi::Handle {
    // types
public:
    // the recipe for releasing my handle
    using traits_type = traitsT;
    // the opaque token mpi gave us
    using handle_type = typename traitsT::handle_type;
    // where the token and its reference count live
    using shared_type = std::shared_ptr<handle_type>;

    // metamethods
public:
    // adopt {handle}; {immortal} marks the ones mpi predefines, which we must never release
    explicit inline Handle(handle_type handle, bool immortal = false);
    // the full set; sharing and stealing are both exactly what {shared_ptr} already does
    inline Handle(const Handle &) = default;
    inline Handle(Handle &&) noexcept = default;
    inline Handle & operator=(const Handle &) = default;
    inline Handle & operator=(Handle &&) noexcept = default;
    inline ~Handle() = default;

    // interface
public:
    // the raw token, for handing to the mpi c api
    inline auto handle() const -> handle_type;
    // the number of owners that currently share my token
    inline auto references() const -> long;

    // implementation details
private:
    // give the token back to mpi and destroy its box; the deleter of a mortal handle
    static inline auto _reclaim(handle_type * box) noexcept -> void;
    // destroy the box but leave the token alone; the deleter of an immortal handle
    static inline auto _abandon(handle_type * box) noexcept -> void;

    // data
private:
    // the token i share with my copies
    shared_type _handle;
};


// get the inline definitions
#include "Handle.icc"


// end of file
