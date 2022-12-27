// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// type alias
using wall_timer_t = pyre::timers::wall_timer_t;


// add bindings timers
void
pyre::py::timers::wall_timers(py::module & m)
{
    // the timer interface
    py::class_<wall_timer_t>(m, "WallTimer")
        // the constructor
        .def(py::init<const wall_timer_t::name_type &>(), "name"_a)

        // accessors
        // the name; read-only property
        .def_property_readonly(
            "name",
            // the implementation
            &wall_timer_t::name,
            // the docstring
            "my name")

        // the registry; read-only static property
        .def_property_readonly_static(
            "registry",
            // the implementation
            [](py::object) -> wall_timer_t::registry_reference { return wall_timer_t::registry(); },
            // the docstring
            "the timer registry")
        // interface
        // start
        .def(
            "start",
            // implementation
            &wall_timer_t::start,
            // docstring
            "start the timer")
        // stop
        .def(
            "stop",
            // implementation
            &wall_timer_t::stop,
            // doctstring
            "stop the timer")
        // reset
        .def(
            "reset",
            // implementation
            &wall_timer_t::reset,
            // docstring
            "reset the timer")
        // read
        .def(
            "read",
            // implementation: by default, always return the interval in seconds to match the
            // expectations of the pure python implementation
            &wall_timer_t::sec,
            // docstring
            "get the accumulated time")
        // as a string, in seconds
        .def(
            "sec",
            // implementation
            &wall_timer_t::sec,
            // docstring
            "render the accumulated time in seconds")
        // as a string, in milliseconds
        .def(
            "ms",
            // implementation
            &wall_timer_t::ms,
            // docstring
            "render the accumulated time in milliseconds")
        // as a string, in microseconds
        .def(
            "us",
            // implementation
            &wall_timer_t::us,
            // docstring
            "render the accumulated time in microseconds")
        // done
        ;

    // all done
    return;
}


// end of file
