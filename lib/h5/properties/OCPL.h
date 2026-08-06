// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "List.h"
// the values my settings trade in
#include "PhaseChange.h"


// the properties shared by every object creation property list
// hdf5 makes this the parent of the dataset and group creation lists, so the settings that
// govern any object one creates — its modification times, the storage of its attributes —
// are declared here once and inherited by both
class pyre::h5::properties::OCPL : public pyre::h5::properties::List {
    // metamethods
public:
    // me
    using self_type = OCPL;
    // my superclass
    using super_type = pyre::h5::properties::List;
    // the full set of special members; there is no public default constructor because
    // object creation properties are always part of a concrete list
    OCPL(const OCPL &) = default;
    OCPL(OCPL &&) noexcept = default;
    OCPL & operator=(const OCPL &) = default;
    OCPL & operator=(OCPL &&) noexcept = default;
    ~OCPL() override = default;

    // interface
public:
    // whether the objects i create record their modification times; turning this off is
    // what makes two runs that produce the same content produce the same bytes
    auto timeTracking() const -> bool;
    // set whether the objects i create record their modification times
    auto timeTracking(bool track) -> void;

    // the thresholds at which attribute storage switches representation, as
    // (max compact, min dense)
    auto attributePhaseChange() const -> PhaseChange;
    // set the attribute storage thresholds
    auto attributePhaseChange(const PhaseChange & thresholds) -> void;

    // whether the order in which attributes were created is tracked and indexed
    auto attributeCreationOrder() const -> CreationOrder;
    // set the attribute creation order flags
    auto attributeCreationOrder(CreationOrder flags) -> void;

    // implementation details
protected:
    // adopt an existing raw handle; for derived lists to pass a freshly created one
    explicit OCPL(id_type id);
};


// end of file
