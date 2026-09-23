// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "OCPL.h"
// the reporting of library refusals
#include "../diagnostics.h"


// adopt an existing raw handle
pyre::h5::properties::OCPL::OCPL(id_type id) : List(id) {}


// whether the objects i create record their modification times
auto
pyre::h5::properties::OCPL::timeTracking() const -> bool
{
    // make room for the answer, in the library's own boolean
    hbool_t track = 0;
    // ask the library
    if (H5Pget_obj_track_times(id(), &track) < 0) {
        // complain if it refused
        complain("pyre.h5.ocpl", "retrieving the time tracking setting");
        // and report that nothing is tracked
        return false;
    }
    // otherwise, report
    return track != 0;
}


// set whether the objects i create record their modification times
auto
pyre::h5::properties::OCPL::timeTracking(bool track) -> void
{
    // hand it to the library
    if (H5Pset_obj_track_times(id(), static_cast<hbool_t>(track)) < 0) {
        // and complain if it refused
        complain("pyre.h5.ocpl", "setting the time tracking");
    }
    // all done
    return;
}


// the thresholds at which attribute storage switches representation
auto
pyre::h5::properties::OCPL::attributePhaseChange() const -> PhaseChange
{
    // make room for the answer
    unsigned int maxCompact = 0;
    unsigned int minDense = 0;
    // ask the library
    if (H5Pget_attr_phase_change(id(), &maxCompact, &minDense) < 0) {
        // complain if it refused
        complain("pyre.h5.ocpl", "retrieving the attribute storage thresholds");
        // and report empty thresholds
        return PhaseChange(0, 0);
    }
    // otherwise, pack and ship
    return PhaseChange(maxCompact, minDense);
}


// set the attribute storage thresholds
auto
pyre::h5::properties::OCPL::attributePhaseChange(const PhaseChange & thresholds) -> void
{
    // hand them to the library
    if (H5Pset_attr_phase_change(id(), thresholds.maxCompact, thresholds.minDense) < 0) {
        // and complain if it refused
        complain("pyre.h5.ocpl", "setting the attribute storage thresholds");
    }
    // all done
    return;
}


// whether the order in which attributes were created is tracked and indexed
auto
pyre::h5::properties::OCPL::attributeCreationOrder() const -> CreationOrder
{
    // make room for the answer
    unsigned int flags = 0;
    // ask the library
    if (H5Pget_attr_creation_order(id(), &flags) < 0) {
        // complain if it refused
        complain("pyre.h5.ocpl", "retrieving the attribute creation order flags");
        // and report that nothing is tracked
        return static_cast<CreationOrder>(0);
    }
    // otherwise, report it in our own vocabulary
    return static_cast<CreationOrder>(flags);
}


// set the attribute creation order flags
auto
pyre::h5::properties::OCPL::attributeCreationOrder(CreationOrder flags) -> void
{
    // hand them to the library
    if (H5Pset_attr_creation_order(id(), static_cast<unsigned int>(flags)) < 0) {
        // and complain if it refused
        complain("pyre.h5.ocpl", "setting the attribute creation order flags");
    }
    // all done
    return;
}


// end of file
