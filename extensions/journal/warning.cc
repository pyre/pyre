// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the warning channel
void
pyre::journal::py::warning(py::module & m)
{
    // type aliases for the member functions (mfp: method pointer)
    // detail
    using getDetail_mfp = warning_t::detail_type (warning_t::*)() const;
    using setDetail_mfp = warning_t & (warning_t::*) (warning_t::detail_type);
    // active
    using getActive_mfp = warning_t::active_type (warning_t::*)() const;
    using setActive_mfp = warning_t & (warning_t::*) (warning_t::active_type);
    // fatal
    using getFatal_mfp = warning_t::fatal_type (warning_t::*)() const;
    using setFatal_mfp = warning_t & (warning_t::*) (warning_t::fatal_type);
    // device
    using getDevice_mfp = warning_t::device_type (warning_t::*)() const;
    using setDevice_mfp = warning_t & (warning_t::*) (warning_t::device_type);


    // the warning channel interface
    py::class_<warning_t>(m, "Warning")
        // the constructor
        .def(
            // the implementation
            py::init<const string_t &>(),
            // the signature
            "name"_a)

        // accessors
        // the name
        .def_property_readonly(
            "name",
            // only getter
            &warning_t::name,
            // the docstring
            "my name")

        // the detail level
        .def_property(
            "detail",
            // the getter
            (getDetail_mfp) &warning_t::detail,
            // the setter
            (setDetail_mfp) &warning_t::detail,
            // the docstring
            "the detail level")

        // the channel activation state; mutable property
        .def_property(
            "active",
            // the getter
            (getActive_mfp) &warning_t::active,
            // the setter
            (setActive_mfp) &warning_t::active,
            // the docstring
            "the channel activation state")

        // the channel activation state; mutable property
        .def_property(
            "fatal",
            // the getter
            (getFatal_mfp) &warning_t::fatal,
            // the setter
            (setFatal_mfp) &warning_t::fatal,
            // the docstring
            "the channel activation state")

        // the registered device: mutable property
        .def_property(
            "device",
            // the getter
            (getDevice_mfp) &warning_t::device,
            // the setter
            (setDevice_mfp) &warning_t::device,
            // the docstring
            "the output device")

        // the contents of the current entry
        .def_property_readonly(
            "page",
            // the getter
            // N.B. the explicit declaration of the λ return value is
            // critical in making the page read/write in python
            [](warning_t & channel) -> pyre::journal::page_t & {
                // get the entry contents
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
            [](warning_t & channel) -> pyre::journal::notes_t & {
                // get the entry notes
                return channel.entry().notes();
            },
            // the docstring
            "the notes associated with the current entry")

        // access to the exception
        .def_property_readonly_static(
            "ApplicationError",
            // the getter
            [m](py::object) -> py::object {
                // this is a module lvel attribute
                return m.attr("ApplicationError");
            },
            // the docstring
            "the exception raised when this channel is fatal")

        // the channel severity
        .def_property_readonly_static(
            "severity",
            // the getter
            [](py::object) -> warning_t::string_type {
                // hardwired, as it is unlikely to change
                return "warning";
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

        // the default activation state
        .def_property_readonly_static(
            "defaultActive",
            // the getter
            [](py::object) -> warning_t::active_type {
                // ask my index
                return warning_t::index().active();
            },
            // the docstring
            "the default state of warning channels")

        // the default fatal state
        .def_property_readonly_static(
            "defaultFatal",
            // the getter
            [](py::object) -> warning_t::fatal_type {
                // ask my index
                return warning_t::index().fatal();
            },
            // the docstring
            "the default fatality of warning channels")

        // the default device: static mutable property
        .def_property_static(
            "defaultDevice",
            // the getter
            [](py::object) -> warning_t::device_type {
                // my index knows
                return warning_t::index().device();
            },
            // the setter
            [](py::object, warning_t::device_type device) -> void {
                // ask my index to set the new device
                warning_t::index().device(device);
                // all done
                return;
            },
            // the docstring
            "the default device for all warning channels")

        // interface
        // activate
        .def(
            "activate",
            // the method;
            &warning_t::activate,
            // the docstring
            "enable output generation")

        // deactivate
        .def(
            "deactivate",
            // the method
            &warning_t::deactivate,
            // the docstring
            "disable output generation")

        // add a line to the contents
        .def(
            "line",
            // the handler
            [](warning_t & channel, const warning_t::string_type & message) -> warning_t & {
                // inject
                channel << message << pyre::journal::newline;
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
            [](warning_t & channel, py::iterable report) -> warning_t & {
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
            [](warning_t & channel, const warning_t::string_type & message) -> warning_t & {
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
            [](const warning_t & channel) -> bool {
                // interpret as a request for the activation state
                return channel.active();
            },
            // the docstring
            "syntactic sugar for checking the state of a channel")

        // send output to a trash can
        .def_static(
            "quiet",
            // the implementation
            &warning_t::quiet,
            // the docstring
            "suppress all output from warning channels")

        // send output to a log file
        .def_static(
            "logfile",
            // the implementation
            [](const warning_t::string_type & path, const warning_t::string_type & mode) -> void {
                // initialize the mode
                auto flag = std::ios_base::out;
                // if {mode} is {append}
                if (mode == "a") {
                    // set the corresponding bit
                    flag |= std::ios_base::app;
                }
                // set up the device
                warning_t::logfile(path, flag);
            },
            // the signature
            "name"_a, "mode"_a = "w",
            // the docstring
            "send all output to a file")

        // done
        ;

    // all done
    return;
}


// end of file
