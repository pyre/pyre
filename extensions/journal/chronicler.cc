// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the chronicler, the object that holds the journal global state
void
pyre::journal::py::
chronicler(py::module & m) {

    // the chronicler interface
    py::class_<chronicler_t>(m, "Chronicler")
        // accessors
        // verbosity
        .def_property_static("verbosity",
                             // the getter
                             [](py::object) {
                                 return chronicler_t::verbosity();
                             },
                             // the setter
                             [](py::object, chronicler_t::verbosity_type verbosity) {
                                 chronicler_t::verbosity(verbosity);
                             },
                             // the docstring
                             "access the maximum verbosity level"
                             )

        // device
        .def_property_static("device",
                             // the getter
                             [](py::object) {
                                 return chronicler_t::device();
                             },
                             // the setter
                             [](py::object, chronicler_t::device_type device) {
                                 chronicler_t::device(device);
                             },
                             // the docstring
                             "access the default device"
                             )

        // global metadata
        .def_property_readonly_static("notes",
                                      // the getter
                                      [] (py::object) -> chronicler_t::notes_type & {
                                          return chronicler_t::notes();
                                      },
                                      // the docstring
                                      "access the global metadata"
                                      )
        // send output to a trash can
        .def_static("quiet",
                    // the implementation
                    &chronicler_t::quiet,
                    // the docstring
                    "suppress all output from all channels"
                    )

         // all done
        ;

    // all done
    return;
}


// end of file
