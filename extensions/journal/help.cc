// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the help channel
void
pyre::journal::py::help(py::module & m)
{
    // type aliases for the member functions (mfp: method pointer)
    // {device} is the only one that confuses {py::overload_cast}
    using getDevice_mfp = help_t::device_type (help_t::*)() const;
    using setDevice_mfp = help_t & (help_t::*)(help_t::device_type);


    // the help channel interface
    auto cls = py::class_<help_t>(m, "Help");
    // the constructor
    cls.def(
        // the implementation
        py::init<const help_t::name_type &, detail_t, dent_t>(),
        // the signature
        "name"_a, "detail"_a = 1, "dent"_a = 0);

    // accessors
    // the name; read-only property
    cls.def_property_readonly(
        "name",
        // only getter
        &help_t::name,
        // the docstring
        "my name");

    // the detail level
    cls.def_property(
        "detail",
        // the getter
        py::overload_cast<>(&help_t::detail, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<help_t::detail_type>(&help_t::detail)),
        // the docstring
        "the detail level");

    // the dent level
    cls.def_property(
        "dent",
        // the getter
        py::overload_cast<>(&help_t::dent, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<help_t::dent_type>(&help_t::dent)),
        // the docstring
        "the dent level");

    // the channel activation state; mutable property
    cls.def_property(
        "active",
        // the getter
        py::overload_cast<>(&help_t::active, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<help_t::active_type>(&help_t::active)),
        // the docstring
        "the channel activation state");

    // the channel fatality; mutable property
    cls.def_property(
        "fatal",
        // the getter
        py::overload_cast<>(&help_t::fatal, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<help_t::fatal_type>(&help_t::fatal)),
        // the docstring
        "whether the channel is fatal");

    // the registered device: mutable property
    cls.def_property(
        "device",
        // the getter
        (getDevice_mfp) &help_t::device,
        // the setter
        pyre::journal::py::setter(cls, (setDevice_mfp) &help_t::device),
        // the docstring
        "the output device");

    // the contents of the current entry
    cls.def_property_readonly(
        "page",
        // the getter
        // N.B. the explicit declaration of the λ return value is
        // critical in making the page read/write in python
        [](help_t & channel) -> pyre::journal::page_t & {
            // get the current entry contents
            return channel.entry().page();
        },
        // the docstring
        "the contents of the current entry");

    // the notes of the current entry
    cls.def_property_readonly(
        "notes",
        // the getter
        // N.B. the explicit declaration of the λ return value is
        // critical in making the notes read/write in python
        [](help_t & channel) -> pyre::journal::notes_t & {
            // get the notes of the current entry
            return channel.entry().notes();
        },
        // the docstring
        "the notes associated with the current entry");

    // access to the exception
    cls.def_property_readonly_static(
        "ApplicationError",
        // the getter
        [m](py::object) -> py::object {
            // this is a module level attribute
            return m.attr("ApplicationError");
        },
        // the docstring
        "the type of exception raised when this channel is fatal");

    // the channel severity: static read-only property
    cls.def_property_readonly_static(
        "severity",
        // the getter
        [](py::object) -> help_t::string_type {
            // hardwired, as it is unlikely to change
            return "help";
        },
        // the docstring
        "get the channel severity name");

    // access to the manager of the global state
    cls.def_property_readonly_static(
        "chronicler",
        // the getter
        [m](py::object) -> py::object {
            // access the class record registered with the module
            return m.attr("Chronicler");
        },
        // the docstring
        "the keeper of the global state");

    // the default activation state
    cls.def_property_readonly_static(
        "defaultActive",
        // the getter
        [](py::object) -> help_t::active_type {
            // my index knows
            return help_t::index().active();
        },
        // the docstring
        "the default state of help channels");

    // the default fatal state
    cls.def_property_readonly_static(
        "defaultFatal",
        // the getter
        [](py::object) -> help_t::fatal_type {
            // my index knows
            return help_t::index().fatal();
        },
        // the docstring
        "the default fatality of help channels");

    // the default device
    cls.def_property_static(
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
        "the default device for all help channels");

    // the default device, for those that prefer methods to class properties
    cls.def_static(
        // the name
        "getDefaultDevice",
        // the implementation
        []() -> help_t::device_type {
            // my index knows
            return help_t::index().device();
        },
        // the docstring
        "get the default device of all help channels");

    // install a new default device
    cls.def_static(
        // the name
        "setDefaultDevice",
        // the implementation
        [](help_t::device_type device) -> help_t::device_type {
            // get the current setting
            auto old = help_t::index().device();
            // install the new device
            help_t::index().device(device);
            // and hand back the previous one
            return old;
        },
        // the signature
        "device"_a,
        // the docstring
        "make {device} the default device of all help channels, and return the previous one");

    // interface
    // activate
    cls.def(
        "activate",
        // the method;
        &help_t::activate,
        // the docstring
        "enable output generation");

    // deactivate
    cls.def(
        "deactivate",
        // the method
        &help_t::deactivate,
        // the docstring
        "disable output generation");

    // dent control
    cls.def(
        "indent",
        // the method;
        &help_t::indent,
        // the signature
        "levels"_a = 1,
        // the docstring
        "indent output by the indicated number of {levels}");

    cls.def(
        "outdent",
        // the method;
        &help_t::outdent,
        // the signature
        "levels"_a = 1,
        // the docstring
        "outdent output by the indicated number of {levels}");

    // add a line to the contents
    cls.def(
        "line",
        // the handler
        [](help_t & channel, const help_t::string_type & message) -> help_t & {
            // inject
            channel << message << pyre::journal::newline;
            // enable chaining
            return channel;
        },
        // the signature
        "message"_a = "",
        // the docstring
        "add another line to the message page");

    // add multiple lines at once
    cls.def(
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
        "add multiple lines to the message page");

    // add a message to the channel and flush
    cls.def(
        "log",
        // the handler
        [](help_t & channel, const help_t::string_type & message,
           // additional arguments are interpreted as entry notes
           py::kwargs kwds) -> help_t & {
            // unpack {kwds}
            for (auto entry : kwds) {
                // and treat each one as a note
                channel << pyre::journal::note(py::str(entry.first), py::str(entry.second));
            }
            // inject and flush
            channel << locator() << message << pyre::journal::endl;
            // enable chaining
            return channel;
        },
        // the signature
        "message"_a = "",
        // the docstring
        "add the optional {message} to the channel contents and then record the entry");

    // operator bool
    cls.def(
        "__bool__",
        // the implementation
        [](const help_t & channel) {
            // interpret as a request for the activation state
            return channel.active();
        },
        // the docstring
        "syntactic sugar for checking the state of a channel");

    // send output to a trash can
    cls.def_static(
        "quiet",
        // the implementation
        &help_t::quiet,
        // the docstring
        "suppress all output from help channels");

    // send output to a log file
    cls.def_static(
        "logfile",
        // the implementation
        [](const help_t::string_type & path, const help_t::string_type & mode) -> void {
            // initialize the mode
            auto flag = std::ios_base::out;
            // if {mode} is {append}
            if (mode == "a") {
                // set the corresponding bit
                flag |= std::ios_base::app;
            }
            // set up the device
            help_t::logfile(path, flag);
            // all done
            return;
        },
        // the signature
        "path"_a, "mode"_a = "w",
        // the docstring
        "send all output to a file");

    // all done
    return;
}


// end of file
