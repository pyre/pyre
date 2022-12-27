// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the chronicler, the object that holds the journal global state
void
pyre::journal::py::chronicler(py::module & m)
{
    // the chronicler interface
    py::class_<chronicler_t>(m, "Chronicler")
        // accessors
        // decor
        .def_property_static(
            "decor",
            // the getter
            [](py::object) -> chronicler_t::detail_type {
                // ask {chronicler_t}
                return chronicler_t::decor();
            },
            // the setter
            [](py::object, chronicler_t::detail_type decor) -> chronicler_t::detail_type {
                // set the new value and return the old
                return chronicler_t::decor(decor);
            },
            // the docstring
            "access the message decoration level")

        // detail
        .def_property_static(
            "detail",
            // the getter
            [](py::object) -> chronicler_t::detail_type {
                // ask {chronicler_t}
                return chronicler_t::detail();
            },
            // the setter
            [](py::object, chronicler_t::detail_type detail) -> chronicler_t::detail_type {
                // set the new value and return the old
                return chronicler_t::detail(detail);
            },
            // the docstring
            "access the maximum detail level")

        // device
        .def_property_static(
            "device",
            // the getter
            [](py::object) -> chronicler_t::device_type {
                // ask {chronicler_t}
                return chronicler_t::device();
            },
            // the setter
            [](py::object, chronicler_t::device_type device) -> void {
                // set the new device
                chronicler_t::device(device);
                // all done
                return;
            },
            // the docstring
            "access the default device")

        // global metadata
        .def_property_readonly_static(
            "notes",
            // the getter
            [](py::object) -> chronicler_t::notes_type & {
                // ask {chronicler_t}
                return chronicler_t::notes();
            },
            // the docstring
            "access the global metadata")

        // send output to a trash can
        .def_static(
            "quiet",
            // the implementation
            &chronicler_t::quiet,
            // the docstring
            "suppress all output from all channels")

        // all done
        ;

    // all done
    return;
}


// end of file
