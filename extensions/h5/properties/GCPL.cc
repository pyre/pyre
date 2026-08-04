// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// group creation property lists
void
pyre::h5::py::properties::gcpl(py::module & m)
{
    // add bindings for hdf5 group creation property lists; they inherit the settings that
    // govern anything one creates from {ocpl}
    auto cls = py::class_<GCPL, OCPL>(
        // in scope
        m,
        // class name
        "gcpl",
        // docstring
        "a group creation property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) -> const GCPL & {
            // easy enough
            return GCPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default group creation property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a group creation property list");

    // interface
    // the link storage thresholds
    cls.def_property(
        // the name
        "linkPhaseChange",
        // the getter
        &GCPL::linkPhaseChange,
        // the setter, which unpacks the {(max compact, min dense)} pair
        [](GCPL & self, const std::tuple<unsigned int, unsigned int> & thresholds) -> void {
            // spread the pair
            auto [maxCompact, minDense] = thresholds;
            // and hand it to the property list
            self.setLinkPhaseChange(maxCompact, minDense);
            // all done
            return;
        },
        // the docstring
        "the thresholds at which link storage switches representation, as "
        "{(max compact, min dense)}");

    // the link creation order flags
    cls.def_property(
        // the name
        "linkCreationOrder",
        // the getter
        &GCPL::linkCreationOrder,
        // the setter
        &GCPL::setLinkCreationOrder,
        // the docstring
        "whether the order in which links were created is tracked and indexed");

    // the expectations that size the object header
    cls.def_property(
        // the name
        "estimatedLinkInfo",
        // the getter
        &GCPL::estimatedLinkInfo,
        // the setter, which unpacks the {(links, name length)} pair
        [](GCPL & self, const std::tuple<unsigned int, unsigned int> & estimate) -> void {
            // spread the pair
            auto [links, nameLength] = estimate;
            // and hand it to the property list
            self.setEstimatedLinkInfo(links, nameLength);
            // all done
            return;
        },
        // the docstring
        "the expected number of links and their average name length, as "
        "{(links, name length)}");

    // all done
    return;
}


// end of file
