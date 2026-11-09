// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the debug channel
void
pyre::journal::py::debug(py::module & m)
{
    // type aliases for the member functions (mfp: method pointer)
    // {device} is the only one that confuses {py::overload_cast}
    using getDevice_mfp = debug_t::device_type (debug_t::*)() const;
    using setDevice_mfp = debug_t & (debug_t::*)(debug_t::device_type);


    // the debug channel interface
    auto cls = py::class_<debug_t>(m, "Debug");
    // the constructor
    cls.def(
        // the implementation
        py::init<const debug_t::name_type &, detail_t, dent_t>(),
        // the signature
        "name"_a, "detail"_a = 1, "dent"_a = 0);

    // accessors
    // the name; read-only property
    cls.def_property_readonly("name", &debug_t::name, "my name");

    // the detail level
    cls.def_property(
        "detail",
        // the getter
        py::overload_cast<>(&debug_t::detail, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<debug_t::detail_type>(&debug_t::detail)),
        // the docstring
        "the detail level");

    // the dent level
    cls.def_property(
        "dent",
        // the getter
        py::overload_cast<>(&debug_t::dent, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<debug_t::dent_type>(&debug_t::dent)),
        // the docstring
        "the dent level");

    // the channel activation state; mutable property
    cls.def_property(
        "active",
        // the getter
        py::overload_cast<>(&debug_t::active, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<debug_t::active_type>(&debug_t::active)),
        // the docstring
        "the channel activation state");

    // the channel fatality; mutable property
    cls.def_property(
        "fatal",
        // the getter
        py::overload_cast<>(&debug_t::fatal, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<debug_t::fatal_type>(&debug_t::fatal)),
        // the docstring
        "whether the channel is fatal");

    // the registered device: mutable property
    cls.def_property(
        "device",
        // the getter
        (getDevice_mfp) &debug_t::device,
        // the setter
        pyre::journal::py::setter(cls, (setDevice_mfp) &debug_t::device),
        // the docstring
        "the output device");

    // the contents of the current entry
    cls.def_property_readonly(
        "page",
        // the getter
        // N.B. the explicit declaration of the λ return value is
        // critical in making the page read/write in python
        [](debug_t & channel) -> pyre::journal::page_t & {
            // get the entry page
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
        [](debug_t & channel) -> pyre::journal::notes_t & {
            // get the entry notes
            return channel.entry().notes();
        },
        // the docstring
        "the notes associated with the current entry");

    // access to the exception
    cls.def_property_readonly_static(
        "DebugError",
        // the getter
        [m](py::object) -> py::object {
            // this is a module level attribute
            return m.attr("DebugError");
        },
        // the docstring
        "the type of exception raised when this channel type is fatal");

    // the channel severity: static read-only property
    cls.def_property_readonly_static(
        "severity",
        // the getter
        [](py::object) -> debug_t::string_type {
            // hardwired, as it is unlikely to change
            return "debug";
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

    // the default activation state: static read-only property
    cls.def_property_readonly_static(
        "defaultActive",
        // the getter
        [](py::object) -> debug_t::active_type {
            // ask my index
            return debug_t::index().active();
        },
        // the docstring
        "the default state of debug channels");

    // the default fatal state: static read-only property
    cls.def_property_readonly_static(
        "defaultFatal",
        // the getter
        [](py::object) -> debug_t::fatal_type {
            // ask my index
            return debug_t::index().fatal();
        },
        // the docstring
        "the default fatality of debug channels");

    // the default device: static mutable property
    cls.def_property_static(
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
        "the default device for all debug channels");

    // the default device, for those that prefer methods to class properties
    cls.def_static(
        // the name
        "getDefaultDevice",
        // the implementation
        []() -> debug_t::device_type {
            // my index knows
            return debug_t::index().device();
        },
        // the docstring
        "get the default device of all debug channels");

    // install a new default device
    cls.def_static(
        // the name
        "setDefaultDevice",
        // the implementation
        [](debug_t::device_type device) -> debug_t::device_type {
            // get the current setting
            auto old = debug_t::index().device();
            // install the new device
            debug_t::index().device(device);
            // and hand back the previous one
            return old;
        },
        // the signature
        "device"_a,
        // the docstring
        "make {device} the default device of all debug channels, and return the previous one");

    // interface
    // activate
    cls.def(
        "activate",
        // the method;
        &debug_t::activate,
        // the docstring
        "enable output generation");

    // deactivate
    cls.def(
        "deactivate",
        // the method
        &debug_t::deactivate,
        // the docstring
        "disable output generation");

    // dent control
    cls.def(
        "indent",
        // the method;
        &debug_t::indent,
        // the signature
        "levels"_a = 1,
        // the docstring
        "indent output by the indicated number of {levels}");

    cls.def(
        "outdent",
        // the method;
        &debug_t::outdent,
        // the signature
        "levels"_a = 1,
        // the docstring
        "outdent output by the indicated number of {levels}");

    // add a line to the contents
    cls.def(
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
        "add another line to the message page");

    // add multiple lines at once
    cls.def(
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
        "add multiple lines to the message page");

    // add a message to the channel and flush
    cls.def(
        "log",
        // the handler
        [](debug_t & channel, const debug_t::string_type & message,
           // additional arguments are interpreted as entry notes
           py::kwargs kwds) -> debug_t & {
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
        [](const debug_t & channel) -> bool {
            // interpret as a request for the activation status
            return channel.active();
        },
        // the docstring
        "syntactic sugar for checking the state of a channel");

    // send output to a trash can
    cls.def_static(
        "quiet",
        // the implementation
        &debug_t::quiet,
        // the docstring
        "suppress all output from debug channels");

    // send output to a log file
    cls.def_static(
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
        "path"_a, "mode"_a = "w",
        // the docstring
        "send all output to a file");

    // all done
    return;
}


// end of file
