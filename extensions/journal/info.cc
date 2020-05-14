// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the info channel
void
pyre::journal::py::
info(py::module & m) {

    // type aliases for the member functions (mfp: method pointer)
    // verbosity
    using getVerbosity_mfp = info_t::verbosity_type (info_t::*)() const;
    using setVerbosity_mfp = info_t & (info_t::*)(info_t::verbosity_type);
    // active
    using getActive_mfp = info_t::active_type (info_t::*)() const;
    using setActive_mfp = info_t & (info_t::*)(info_t::active_type);
    // fatal
    using getFatal_mfp = info_t::fatal_type (info_t::*)() const;
    using setFatal_mfp = info_t & (info_t::*)(info_t::fatal_type);
    // device
    using getDevice_mfp = info_t::device_type (info_t::*)() const;
    using setDevice_mfp = info_t & (info_t::*)(info_t::device_type);


    // the info channel interface
    py::class_<info_t>(m, "Informational")
        // the constructor
        .def(py::init<const string_t &>(), "name"_a)

        // accessors
        // the name; read-only property
        .def_property_readonly("name",
                               &info_t::name,
                               "my name")

        // the verbosity level
        .def_property("verbosity",
                      // the getter
                      (getVerbosity_mfp) &info_t::verbosity,
                      // the setter
                      (setVerbosity_mfp) &info_t::verbosity,
                      // the docstring
                      "the verbosity level"
                      )

        // the channel activation state; mutable property
        .def_property("active",
                      // the getter
                      (getActive_mfp) &info_t::active,
                      // the setter
                      (setActive_mfp) &info_t::active,
                      // the docstring
                      "the channel activation state"
                      )

        // the channel activation state; mutable property
        .def_property("fatal",
                      // the getter
                      (getFatal_mfp) &info_t::fatal,
                      // the setter
                      (setFatal_mfp) &info_t::fatal,
                      // the docstring
                      "the channel activation state"
                      )

        // the registered device: mutable property
        .def_property("device",
                      // the getter
                      (getDevice_mfp) &info_t::device,
                      // the setter
                      (setDevice_mfp) &info_t::device,
                      // the docstring
                      "the output device"
                      )

        // the content of the current entry
        .def_property_readonly("page",
                               // the getter
                               // N.B. the explicit declaration of the λ return value is
                               // critical in making the page read/write in python
                               [] (info_t & channel) -> pyre::journal::page_t & {
                                   return channel.entry().page();
                               },
                               // the docstring
                               "the contents of the current entry"
                      )

        // the notes of the current entry
        .def_property_readonly("notes",
                               // the getter
                               // N.B. the explicit declaration of the λ return value is
                               // critical in making the notes read/write in python
                               [] (info_t & channel) -> pyre::journal::notes_t & {
                                   return channel.entry().notes();
                               },
                               // the docstring
                               "the notes associated with the current entry"
                      )

        // access to the exception
        .def_property_readonly_static("ApplicationError",
                                      // the getter
                                      [m](py::object) -> py::object {
                                          return m.attr("ApplicationError");
                                      },
                                      // the docstring
                                      "the keeper of the global state"
                                      )

        // the channel severity: static read-only property
        .def_property_readonly_static("severity",
                                      // the getter
                                      [](py::object) -> info_t::string_type {
                                          return "info";
                                      },
                                      // the docstring
                                      "get the channel severity name"
                                      )

        // access to the manager of the global state
        .def_property_readonly_static("chronicler",
                                      // the getter
                                      [m](py::object) -> py::object {
                                          return m.attr("Chronicler");
                                      },
                                      // the docstring
                                      "the keeper of the global state"
                                      )

        // the default activation state: static read-only property
        .def_property_readonly_static("defaultActive",
                                      // the getter
                                      [](py::object) -> info_t::active_type {
                                          return info_t::index().active();
                                      },
                                      // the docstring
                                      "the default state of info channels"
                                      )

        // the default fatal state: static read-only property
        .def_property_readonly_static("defaultFatal",
                                      // the getter
                                      [](py::object) -> info_t::fatal_type {
                                          return info_t::index().fatal();
                                      },
                                      // the docstring
                                      "the default fatality of info channels"
                                      )

        // the default device: static mutable property
        .def_property_static("defaultDevice",
                             // the getter
                             [](py::object) -> info_t::device_type {
                                 return info_t::index().device();
                             },
                             // the setter
                             [](py::object, info_t::device_type device) {
                                 info_t::index().device(device);
                             },
                             // the docstring
                             "the default device for all info channels"
                             )

        // interface
        // activate
        .def("activate",
             // the method;
             &info_t::activate,
             // the docstring
             "enable output generation"
             )

        // deactivate
        .def("deactivate",
             // the method
             &info_t::deactivate,
             // the docstring
             "disable output generation"
             )

        // add a line to the contents
        .def("line",
             // the handler
             [](info_t & channel, const info_t::string_type & message) {
                 // inject
                 channel << message << pyre::journal::newline;
             },
             // the docstring
             "add another line to the message page",
             // the arguments
             "message"_a = ""
             )

        // add a message to the channel and flush
        .def("log",
             // the handler
             [](info_t & channel, const info_t::string_type & message) {
                 // inject and flush
                 channel << message << pyre::journal::endl;
             },
             // the docstring
             "add the optional {message} to the channel contents and then record the entry",
             // the arguments
             "message"_a = ""
             )

        // operator bool
        .def("__bool__",
             // the implementation
             [](const info_t & channel) { return channel.active(); },
             // the docstring
             "syntactic sugar for checking the state of a channel"
             )

        // send output to a trash can
        .def_static("quiet",
                    // the implementation
                    &info_t::quiet,
                    // the docstring
                    "suppress all output from info channels"
                    )

        // send output to a log file
        .def_static("logfile",
                    // the implementation
                    [](const info_t::string_type & path) {
                        info_t::logfile(path);
                    },
                    // the docstring
                    "send all output to a file",
                    // the arguments
                    "name"_a
                    )

         // done
        ;

    // all done
    return;
}


// end of file
