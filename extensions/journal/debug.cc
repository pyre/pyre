// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the debug channel
void
pyre::journal::py::debug(py::module & m)
{
    // type aliases for the member functions (mfp: method pointer)
    // detail
    using getDetail_mfp = debug_t::detail_type (debug_t::*)() const;
    using setDetail_mfp = debug_t & (debug_t::*) (debug_t::detail_type);
    // active
    using getActive_mfp = debug_t::active_type (debug_t::*)() const;
    using setActive_mfp = debug_t & (debug_t::*) (debug_t::active_type);
    // fatal
    using getFatal_mfp = debug_t::fatal_type (debug_t::*)() const;
    using setFatal_mfp = debug_t & (debug_t::*) (debug_t::fatal_type);
    // device
    using getDevice_mfp = debug_t::device_type (debug_t::*)() const;
    using setDevice_mfp = debug_t & (debug_t::*) (debug_t::device_type);


    // the debug channel interface
    py::class_<debug_t>(m, "Debug")
        // the constructor
        .def(
            // the implementation
            py::init<const debug_t::name_type &>(),
            // the signature
            "name"_a)

        // accessors
        // the name; read-only property
        .def_property_readonly("name", &debug_t::name, "my name")

        // the detail level
        .def_property(
            "detail",
            // the getter
            (getDetail_mfp) &debug_t::detail,
            // the setter
            (setDetail_mfp) &debug_t::detail,
            // the docstring
            "the detail level")

        // the channel activation state; mutable property
        .def_property(
            "active",
            // the getter
            (getActive_mfp) &debug_t::active,
            // the setter
            (setActive_mfp) &debug_t::active,
            // the docstring
            "the channel activation state")

        // the channel activation state; mutable property
        .def_property(
            "fatal",
            // the getter
            (getFatal_mfp) &debug_t::fatal,
            // the setter
            (setFatal_mfp) &debug_t::fatal,
            // the docstring
            "the channel activation state")

        // the registered device: mutable property
        .def_property(
            "device",
            // the getter
            (getDevice_mfp) &debug_t::device,
            // the setter
            (setDevice_mfp) &debug_t::device,
            // the docstring
            "the output device")

        // the contents of the current entry
        .def_property_readonly(
            "page",
            // the getter
            // N.B. the explicit declaration of the λ return value is
            // critical in making the page read/write in python
            [](debug_t & channel) -> pyre::journal::page_t & {
                // get the entry page
                return channel.entry().page();
            },
            // the docstring
            "the contents of the current entry")

        // the notes of the current entry
        .def_property_readonly(
            "notes",
            // the getter
            // N.B. the explicit declaration of the λ return value is
            // critical in making the notes read/write in python
            [](debug_t & channel) -> pyre::journal::notes_t & {
                // get the entry notes
                return channel.entry().notes();
            },
            // the docstring
            "the notes associated with the current entry")

        // access to the exception
        .def_property_readonly_static(
            "DebugError",
            // the getter
            [m](py::object) -> py::object {
                // this is a module level attribute
                return m.attr("DebugError");
            },
            // the docstring
            "the type of exception raised when this channel type is fatal")

        // the channel severity: static read-only property
        .def_property_readonly_static(
            "severity",
            // the getter
            [](py::object) -> debug_t::string_type {
                // hardwired, as it is unlikely to change
                return "debug";
            },
            // the docstring
            "get the channel severity name")

        // access to the manager of the global state
        .def_property_readonly_static(
            "chronicler",
            // the getter
            [m](py::object) -> py::object {
                // access the class record registered with the module
                return m.attr("Chronicler");
            },
            // the docstring
            "the keeper of the global state")

        // the default activation state: static read-only property
        .def_property_readonly_static(
            "defaultActive",
            // the getter
            [](py::object) -> debug_t::active_type {
                // ask my index
                return debug_t::index().active();
            },
            // the docstring
            "the default state of debug channels")

        // the default fatal state: static read-only property
        .def_property_readonly_static(
            "defaultFatal",
            // the getter
            [](py::object) -> debug_t::fatal_type {
                // ask my index
                return debug_t::index().fatal();
            },
            // the docstring
            "the default fatality of debug channels")

        // the default device: static mutable property
        .def_property_static(
            "defaultDevice",
            // the getter
            [](py::object) -> debug_t::device_type {
                // my index knows
                return debug_t::index().device();
            },
            // the setter
            [](py::object, debug_t::device_type device) {
                // ask my index to set the new device
                debug_t::index().device(device);
            },
            // the docstring
            "the default device for all debug channels")

        // interface
        // activate
        .def(
            "activate",
            // the method;
            &debug_t::activate,
            // the docstring
            "enable output generation")

        // deactivate
        .def(
            "deactivate",
            // the method
            &debug_t::deactivate,
            // the docstring
            "disable output generation")

        // add a line to the contents
        .def(
            "line",
            // the handler
            [](debug_t & channel, const debug_t::string_type & message) -> debug_t & {
                // inject
                channel << py::str(message) << pyre::journal::newline;
                // enable chaining
                return channel;
            },
            // the signature
            "message"_a = "",
            // the docstring
            "add another line to the message page")

        // add multiple lines at once
        .def(
            "report",
            // the handler
            [](debug_t & channel, py::iterable report) -> debug_t & {
                // extract individual lines from the iterable
                for (auto line : report) {
                    // and inject each one
                    channel << py::str(line) << pyre::journal::newline;
                }
                // all done
                return channel;
            },
            // the signature
            "report"_a,
            // the docstring
            "add multiple lines to the message page")

        // add a message to the channel and flush
        .def(
            "log",
            // the handler
            [](debug_t & channel, const debug_t::string_type & message) -> debug_t & {
                // inject and flush
                channel << locator() << message << pyre::journal::endl;
                // enable chaining
                return channel;
            },
            // the signature
            "message"_a = "",
            // the docstring
            "add the optional {message} to the channel contents and then record the entry")

        // operator bool
        .def(
            "__bool__",
            // the implementation
            [](const debug_t & channel) -> bool {
                // interpret as a request for the activation status
                return channel.active();
            },
            // the docstring
            "syntactic sugar for checking the state of a channel")

        // send output to a trash can
        .def_static(
            "quiet",
            // the implementation
            &debug_t::quiet,
            // the docstring
            "suppress all output from debug channels")

        // send output to a log file
        .def_static(
            "logfile",
            // the implementation
            [](const debug_t::string_type & path, const debug_t::string_type & mode) -> void {
                // initialize the mode
                auto flag = std::ios_base::out;
                // if {mode} is {append}
                if (mode == "a") {
                    // set the corresponding bit
                    flag |= std::ios_base::app;
                }
                // set up the device
                debug_t::logfile(path, flag);
            },
            // the arguments
            "name"_a, "mode"_a = "w",
            // the docstring
            "send all output to a file")

        // done
        ;

    // all done
    return;
}


// end of file
