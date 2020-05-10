// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings to the inventory
void
pyre::libjournal::
devices(py::module & m) {
    // the base device
    py::class_<device_t, device_t::pointer_type>(m, "Device")
        // accessor
        .def_property_readonly("name", &device_t::name, "the name of the device")
        // done
        ;

    // the trash can
    py::class_<trash_t, device_t, trash_t::pointer_type>(m, "Trash")
        // constructor
        .def(py::init<>())
        // done
        ;

    // the streaming device
    py::class_<stream_t, stream_t::pointer_type, device_t>(m, "Stream")
        // constructor
        .def(py::init<const stream_t::name_type &, stream_t::stream_type &>())
        // done
        ;

    // the console
    py::class_<cout_t, cout_t::pointer_type, stream_t>(m, "Console")
        // constructor
        .def(py::init<>())
        // done
        ;

    // the streaming device
    py::class_<cerr_t, cerr_t::pointer_type, stream_t>(m, "ErrorConsole")
        // constructor
        .def(py::init<>())
        // done
        ;

    // all done
    return;
}


// end of file
