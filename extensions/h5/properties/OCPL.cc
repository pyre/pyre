// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// object creation property lists
void
pyre::h5::py::properties::ocpl(py::module & m)
{
    // add bindings for the properties shared by every object creation property list; there is
    // no constructor, since these settings are always part of a concrete list
    auto cls = py::class_<OCPL, PropList>(
        // in scope
        m,
        // class name
        "ocpl",
        // docstring
        "the properties shared by every object creation property list");

    // interface
    // whether the objects being created record their modification times
    cls.def_property(
        // the name
        "trackTimes",
        // the getter
        &OCPL::trackTimes,
        // the setter
        &OCPL::setTrackTimes,
        // the docstring
        "whether the objects i create record their modification times");

    // the attribute storage thresholds
    cls.def_property(
        // the name
        "attributePhaseChange",
        // the getter
        &OCPL::attributePhaseChange,
        // the setter, which unpacks the {(max compact, min dense)} pair
        [](OCPL & self, const std::tuple<unsigned int, unsigned int> & thresholds) -> void {
            // spread the pair
            auto [maxCompact, minDense] = thresholds;
            // and hand it to the property list
            self.setAttributePhaseChange(maxCompact, minDense);
            // all done
            return;
        },
        // the docstring
        "the thresholds at which attribute storage switches representation, as "
        "{(max compact, min dense)}");

    // the attribute creation order flags
    cls.def_property(
        // the name
        "attributeCreationOrder",
        // the getter
        &OCPL::attributeCreationOrder,
        // the setter
        &OCPL::setAttributeCreationOrder,
        // the docstring
        "whether the order in which attributes were created is tracked and indexed");

    // all done
    return;
}


// end of file
