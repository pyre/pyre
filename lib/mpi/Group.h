// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// the owner of my handle, and the recipe it uses to release it
#include "traits.h"
#include "Handle.h"


// a set of processes, ordered so that each one has a rank within the set
class pyre::mpi::Group {
    // types
public:
    // me
    using self_type = Group;
    // the opaque token mpi uses to name a group
    using handle_type = MPI_Group;
    // the shared owner of that token
    using storage_type = Handle<GroupHandle>;
    // a collection of ranks, e.g. the members i am asked to keep or drop
    using ranks_type = ranks_t;

    // metamethods
public:
    // adopt an existing {handle}; {immortal} marks the groups mpi predefines
    explicit inline Group(handle_type handle, bool immortal = false);
    // the full set; copies share the handle, moves steal it
    inline Group(const Group &) = default;
    inline Group(Group &&) noexcept = default;
    inline Group & operator=(const Group &) = default;
    inline Group & operator=(Group &&) noexcept = default;
    inline ~Group() = default;

    // interface
public:
    // the raw token, for handing to the mpi c api
    inline auto handle() const -> handle_type;
    // whether i name no group at all, as opposed to a group with no members
    inline auto isNull() const -> bool;
    // whether i have no members
    inline auto isEmpty() const -> bool;
    // contextual conversion to {bool}, true when i name a group
    explicit inline operator bool() const;

    // the rank of the calling process within me, or {undefined} when it is not a member
    inline auto rank() const -> rank_t;
    // how many processes i hold
    inline auto size() const -> size_type;

    // build the group that holds exactly the members named in {ranks}, in that order
    inline auto include(const ranks_type & ranks) const -> Group;
    // build the group that holds all my members except those named in {ranks}
    inline auto exclude(const ranks_type & ranks) const -> Group;

    // how my membership relates to {other}'s
    inline auto compare(const Group & other) const -> Comparison;
    // the ranks that my members {ranks} carry in {other}
    inline auto translateRanks(const ranks_type & ranks, const Group & other) const -> ranks_type;

    // data
private:
    // the token i own
    storage_type _handle;
};


// get the inline definitions
#include "Group.icc"


// end of file
