// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"


// the shared owner of a libpq object
//
// libpq keeps no reference count of its own for the sessions and result sets it hands out, so
// we supply one. the count lives in a {std::shared_ptr}, which makes it atomic, makes copies
// and moves free, and makes the release path exception safe: the last owner to go away is the
// one that hands the object back
//
// what the pointer owns is not the libpq object but a box holding a pointer to it. the extra
// hop is what lets {release} do its job: closing a session nulls the box, and every copy of the
// handle, wherever it has got to, sees the null and refuses to go on. a design that shared the
// libpq pointer directly could not do this, and would leave every other copy holding an address
// that libpq had already freed
template <class traitsT>
class pyre::postgres::Handle {
    // types
public:
    // the recipe for releasing my object
    using traits_type = traitsT;
    // the opaque pointer libpq gave us
    using handle_type = typename traitsT::handle_type;
    // the box the pointer lives in, and where its reference count lives
    using shared_type = std::shared_ptr<handle_type>;

    // metamethods
public:
    // adopt {handle}
    explicit inline Handle(handle_type handle);
    // the full set; sharing and stealing are both exactly what {shared_ptr} already does
    inline Handle(const Handle &) = default;
    inline Handle(Handle &&) noexcept = default;
    inline Handle & operator=(const Handle &) = default;
    inline Handle & operator=(Handle &&) noexcept = default;
    inline ~Handle() = default;

    // interface
public:
    // the raw pointer, for handing to the libpq c api; null once i have been released
    inline auto handle() const -> handle_type;
    // whether i still name a live libpq object
    inline auto valid() const -> bool;
    // the number of owners that currently share my box
    inline auto references() const -> long;

    // give the object back to libpq now, rather than when the last owner goes away. every owner
    // of this box observes the release, so a session that has been closed cannot be used through
    // a copy of the handle that closed it
    inline auto release() -> void;

    // implementation details
private:
    // release the object, if it is still there, and destroy its box
    static inline auto _reclaim(handle_type * box) noexcept -> void;

    // data
private:
    // the box i share with my copies
    shared_type _handle;
};


// get the inline definitions
#include "Handle.icc"


// end of file
