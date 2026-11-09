// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// register the class of the timeline, so that every signature can name it
void
pyre::py::geometry::timelineClass(py::module & m)
{
    // register the timeline
    py::class_<timeline_t>(
        // the scope
        m,
        // the name of the class
        "Timeline",
        // its docstring
        "the affine line of time, whose instants are known by their seconds since its epoch");

    // all done
    return;
}


// bind the timeline; its points are known by their coordinates, the seconds since its epoch,
// and the calendar that names them belongs to the python layer
void
pyre::py::geometry::timeline()
{
    // the coordinate of the timeline
    using coordinate_t = timeline_t::coordinate_type;
    // the civil calendar
    using calendar_t = timeline_t::time_type;
    // the durations
    using duration_t = timeline_t::vector_type;

    // the class of the timeline, registered by {timelineClass}
    auto cls = py::class_<timeline_t>(py::type::of<timeline_t>());

    // build a timeline
    cls.def(
        // the constructor, from the seconds of the epoch past the start of 1970 in UTC
        py::init([](coordinate_t epoch) {
            // the epoch, on the civil calendar
            return timeline_t(calendar_t(duration_t(epoch)));
        }),
        // the signature
        "epoch"_a = 0.0,
        // the docstring
        "a timeline whose epoch is {epoch} seconds after the start of 1970, in UTC");

    // the epoch
    cls.def_property_readonly(
        // the name
        "epoch",
        // the implementation
        [](const timeline_t & self) {
            // its seconds past the start of 1970, in UTC
            return self.epoch().time_since_epoch().count();
        },
        // the docstring
        "the seconds of my epoch past the start of 1970, in UTC");

    // the instant at a coordinate
    cls.def(
        // the name
        "point",
        // the implementation
        [](const timeline_t &, coordinate_t coordinate) {
            // the instant that many seconds past the epoch
            return instant_t(timeline_t::fromCoordinate(coordinate));
        },
        // the signature
        "coordinate"_a,
        // the docstring
        "the instant {coordinate} seconds past my epoch");

    // the interval between two coordinates
    cls.def(
        // the name
        "interval",
        // the implementation
        [](const timeline_t &, coordinate_t lower, coordinate_t upper) {
            // the instants at the two coordinates, and the interval between them
            return interval_t(
                instant_t(timeline_t::fromCoordinate(lower)),
                instant_t(timeline_t::fromCoordinate(upper)));
        },
        // the signature
        "lower"_a, "upper"_a,
        // the docstring
        "the instants from {lower} to {upper} seconds past my epoch; an infinite end leaves the "
        "interval unbounded on its side");

    // the time between two instants
    cls.def(
        // the name
        "distance",
        // the implementation
        &timeline_t::distance,
        // the signature
        "p"_a, "q"_a,
        // the docstring
        "the seconds between the instants {p} and {q}");

    // all done
    return;
}


// end of file
