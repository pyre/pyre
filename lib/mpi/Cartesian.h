// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"

// my superclass
#include "Communicator.h"


// a communicator whose processes are arranged on a grid, so that each one can name its
// neighbors by walking along an axis instead of by computing ranks
class pyre::mpi::Cartesian : public pyre::mpi::Communicator {
    // types
public:
    // me
    using self_type = Cartesian;
    // my superclass
    using super_type = pyre::mpi::Communicator;
    // the coordinates of a process on the grid, and the extent of the grid itself
    using shape_type = shape_t;

    // metamethods
public:
    // adopt an existing {handle}, which must already carry a cartesian topology
    explicit inline Cartesian(handle_type handle, bool immortal = false);
    // the full set; a cartesian communicator is a communicator
    inline Cartesian(const Cartesian &) = default;
    inline Cartesian(Cartesian &&) noexcept = default;
    inline Cartesian & operator=(const Cartesian &) = default;
    inline Cartesian & operator=(Cartesian &&) noexcept = default;
    inline ~Cartesian() = default;

    // interface
public:
    // how many axes my grid has
    inline auto dimensions() const -> size_type;
    // the extent of my grid along each axis
    inline auto shape() const -> shape_type;
    // which of my axes wrap around
    inline auto periods() const -> shape_type;

    // where the process of the given {rank} sits on my grid
    inline auto coordinates(rank_t rank) const -> shape_type;
    // the rank of the process that sits at {coordinates}
    inline auto rank(const shape_type & coordinates) const -> rank_t;
    // the overload above would otherwise hide the inherited {rank()}, which answers the far
    // more common question of where the calling process sits
    using Communicator::rank;

    // the ranks of the two processes {displacement} steps away along {direction}: the one that
    // would send to me, and the one i would send to. either comes back as {procNull} when the
    // axis does not wrap and the walk falls off its end
    inline auto shift(int direction, int displacement) const -> std::pair<rank_t, rank_t>;

    // the sub-grid spanned by the axes flagged in {keep}
    inline auto sub(const shape_type & keep) const -> Cartesian;
};


// get the inline definitions
#include "Cartesian.icc"


// end of file
