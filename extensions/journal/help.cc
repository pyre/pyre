// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the help channel
void
pyre::journal::py::help(py::module & m)
{
    // type aliases for the member functions (mfp: method pointer)
    // detail
    using getDetail_mfp = help_t::detail_type (help_t::*)() const;
    using setDetail_mfp = help_t & (help_t::*) (help_t::detail_type);
    // active
    using getActive_mfp = help_t::active_type (help_t::*)() const;
    using setActive_mfp = help_t & (help_t::*) (help_t::active_type);
    // fatal
    using getFatal_mfp = help_t::fatal_type (help_t::*)() const;
    using setFatal_mfp = help_t & (help_t::*) (help_t::fatal_type);
    // device
    using getDevice_mfp = help_t::device_type (help_t::*)() const;
    using setDevice_mfp = help_t & (help_t::*) (help_t::device_type);


    // the help channel interface
    py::class_<help_t>(m, "Help")
        // the constructor
        .def(
            // the implementation
            py::init<const help_t::name_type &>(),
            // the signature
            "name"_a)

        // accessors
        // the name; read-only property
        .def_property_readonly(
            "name",
            // only getter
            &help_t::name,
            // the docstring
            "my name")

        // the detail level
        .def_property(
            "detail",
            // the getter
            (getDetail_mfp) &help_t::detail,
            // the setter
            (setDetail_mfp) &help_t::detail,
            // the docstring
            "the detail level")

        // the channel activation state; mutable property
        .def_property(
            "active",
            // the getter
            (getActive_mfp) &help_t::active,
            // the setter
            (setActive_mfp) &help_t::active,
            // the docstring
            "the channel activation state")

        // the channel activation state; mutable property
        .def_property(
            "fatal",
            // the getter
            (getFatal_mfp) &help_t::fatal,
            // the setter
            (setFatal_mfp) &help_t::fatal,
            // the docstring
            "the channel activation state")

        // the registered device: mutable property
        .def_property(
            "device",
            // the getter
            (getDevice_mfp) &help_t::device,
            // the setter
            (setDevice_mfp) &help_t::device,
            // the docstring
            "the output device")

        // the contents of the current entry
        .def_property_readonly(
            "page",
            // the getter
            // N.B. the explicit declaration of the λ return value is
            // critical in making the page read/write in python
            [](help_t & channel) -> pyre::journal::page_t & {
                // get the current entry contents
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
            [](help_t & channel) -> pyre::journal::notes_t & {
                // get the notes of the current entry
                return channel.entry().notes();
            },
            // the docstring
            "the notes associated with the current entry")

        // access to the exception
        .def_property_readonly_static(
            "ApplicationError",
            // the getter
            [m](py::object) -> py::object {
                // this is a module level attribute
                return m.attr("ApplicationError");
            },
            // the docstring
            "the type of exception raised when this channel is fatal")

        // the channel severity: static read-only property
        .def_property_readonly_static(
            "severity",
            // the getter
            [](py::object) -> help_t::string_type {
                // hardwired, as it is unlikely to change
                return "help";
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
            [](py::object) -> help_t::active_type {
                // my index knows
                return help_t::index().active();
            },
            // the docstring
            "the default state of help channels")

        // the default fatal state
        .def_property_readonly_static(
            "defaultFatal",
            // the getter
            [](py::object) -> help_t::fatal_type {
                // my index knows
                return help_t::index().fatal();
            },
            // the docstring
            "the default fatality of help channels")

        // the default device
        .def_property_static(
            "defaultDevice",
            // the getter
            [](py::object) -> help_t::device_type {
                // my index knows
                return help_t::index().device();
            },
            // the setter
            [](py::object, help_t::device_type device) -> void {
                // ask my index to set the default device
                help_t::index().device(device);
                // all done
                return;
            },
            // the docstring
            "the default device for all help channels")

        // interface
        // activate
        .def(
            "activate",
            // the method;
            &help_t::activate,
            // the docstring
            "enable output generation")

        // deactivate
        .def(
            "deactivate",
            // the method
            &help_t::deactivate,
            // the docstring
            "disable output generation")

        // add a line to the contents
        .def(
            "line",
            // the handler
            [](help_t & channel, help_t::string_type message) -> help_t & {
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
            [](help_t & channel, py::iterable report) -> help_t & {
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
            [](help_t & channel, help_t::string_type message) -> help_t & {
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
            [](const help_t & channel) {
                // interpret as a request for the activation state
                return channel.active();
            },
            // the docstring
            "syntactic sugar for checking the state of a channel")

        // send output to a trash can
        .def_static(
            "quiet",
            // the implementation
            &help_t::quiet,
            // the docstring
            "suppress all output from help channels")

        // send output to a log file
        .def_static(
            "logfile",
            // the implementation
            [](const help_t::string_type & path) -> void {
                // set up the device
                help_t::logfile(path);
                // all done
                return;
            },
            // the signature
            "name"_a,
            // the docstring
            "send all output to a file")

        // done
        ;

    // all done
    return;
}


// end of file