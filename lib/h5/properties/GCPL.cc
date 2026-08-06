// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "GCPL.h"


// make a fresh group creation property list
pyre::h5::properties::GCPL::GCPL() : OCPL(H5Pcreate(H5P_GROUP_CREATE)) {}


// adopt an existing raw handle
pyre::h5::properties::GCPL::GCPL(id_type id) : OCPL(id) {}


// the shared default group creation property list
auto
pyre::h5::properties::GCPL::theDefault() -> const GCPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const GCPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


// the thresholds at which link storage switches representation
auto
pyre::h5::properties::GCPL::linkPhaseChange() const -> PhaseChange
{
    // make room for the answer
    unsigned int maxCompact = 0;
    unsigned int minDense = 0;
    // ask the library
    H5Pget_link_phase_change(id(), &maxCompact, &minDense);
    // pack and ship
    return PhaseChange(maxCompact, minDense);
}


// set the link storage thresholds
auto
pyre::h5::properties::GCPL::linkPhaseChange(const PhaseChange & thresholds) -> void
{
    // hand them to the library
    H5Pset_link_phase_change(id(), thresholds.maxCompact, thresholds.minDense);
    // all done
    return;
}


// whether the order in which links were created is tracked and indexed
auto
pyre::h5::properties::GCPL::linkCreationOrder() const -> CreationOrder
{
    // make room for the answer
    unsigned int flags = 0;
    // ask the library
    H5Pget_link_creation_order(id(), &flags);
    // and report it in our own vocabulary
    return static_cast<CreationOrder>(flags);
}


// set the link creation order flags
auto
pyre::h5::properties::GCPL::linkCreationOrder(CreationOrder flags) -> void
{
    // hand them to the library
    H5Pset_link_creation_order(id(), static_cast<unsigned int>(flags));
    // all done
    return;
}


// the expectations that size my object header
auto
pyre::h5::properties::GCPL::estimatedLinkInfo() const -> LinkEstimate
{
    // make room for the answer
    unsigned int links = 0;
    unsigned int nameLength = 0;
    // ask the library
    H5Pget_est_link_info(id(), &links, &nameLength);
    // pack and ship
    return LinkEstimate(links, nameLength);
}


// set the expected number of links and their average name length
auto
pyre::h5::properties::GCPL::estimatedLinkInfo(const LinkEstimate & estimate) -> void
{
    // hand them to the library
    H5Pset_est_link_info(id(), estimate.links, estimate.nameLength);
    // all done
    return;
}


// end of file
