// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the error channel
void
pyre::journal::py::error(py::module & m)
{
    // type aliases for the member functions (mfp: method pointer)
    // {device} is the only one that confuses {py::overload_cast}
    using getDevice_mfp = error_t::device_type (error_t::*)() const;
    using setDevice_mfp = error_t & (error_t::*)(error_t::device_type);


    // the error channel interface
    auto cls = py::class_<error_t>(m, "Error");
    // the constructor
    cls.def(
        // the implementation
        py::init<const error_t::name_type &, detail_t, dent_t>(),
        // the signature
        "name"_a, "detail"_a = 1, "dent"_a = 0);

    // accessors
    // the name; read-only property
    cls.def_property_readonly(
        "name",
        // only getter
        &error_t::name,
        // the docstring
        "my name");

    // the detail level
    cls.def_property(
        "detail",
        // the getter
        py::overload_cast<>(&error_t::detail, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<error_t::detail_type>(&error_t::detail)),
        // the docstring
        "the detail level");

    // the dent level
    cls.def_property(
        "dent",
        // the getter
        py::overload_cast<>(&error_t::dent, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<error_t::dent_type>(&error_t::dent)),
        // the docstring
        "the dent level");

    // the channel activation state; mutable property
    cls.def_property(
        "active",
        // the getter
        py::overload_cast<>(&error_t::active, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<error_t::active_type>(&error_t::active)),
        // the docstring
        "the channel activation state");

    // the channel fatality; mutable property
    cls.def_property(
        "fatal",
        // the getter
        py::overload_cast<>(&error_t::fatal, py::const_),
        // the setter
        pyre::journal::py::setter(cls, py::overload_cast<error_t::fatal_type>(&error_t::fatal)),
        // the docstring
        "whether the channel is fatal");

    // the registered device: mutable property
    cls.def_property(
        "device",
        // the getter
        (getDevice_mfp) &error_t::device,
        // the setter
        pyre::journal::py::setter(cls, (setDevice_mfp) &error_t::device),
        // the docstring
        "the output device");

    // the content of the current entry
    cls.def_property_readonly(
        "page",
        // the getter
        // N.B. the explicit declaration of the λ return value is
        // critical in making the page read/write in python
        [](error_t & channel) -> pyre::journal::page_t & {
            // ask {chronicler_t}
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
        [](error_t & channel) -> pyre::journal::notes_t & {
            // ask {chronicler_t}
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
        "the keeper of the global state");

    // the channel severity
    cls.def_property_readonly_static(
        "severity",
        // the getter
        [](py::object) -> error_t::string_type {
            // hardwired, as it's unlikely to ever change
            return "error";
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
        [](py::object) -> error_t::active_type {
            // ask my index
            return error_t::index().active();
        },
        // the docstring
        "the default state of error channels");

    // the default fatal state: static read-only property
    cls.def_property_readonly_static(
        "defaultFatal",
        // the getter
        [](py::object) -> error_t::fatal_type {
            // ask my index
            return error_t::index().fatal();
        },
        // the docstring
        "the default fatality of error channels");

    // the default device: static mutable property
    cls.def_property_static(
        "defaultDevice",
        // the getter
        [](py::object) -> error_t::device_type {
            // my index knows
            return error_t::index().device();
        },
        // the setter
        [](py::object, error_t::device_type device) -> void {
            // ask my index to set the new device
            error_t::index().device(device);
            // all done
            return;
        },
        // the docstring
        "the default device for all error channels");

    // the default device, for those that prefer methods to class properties
    cls.def_static(
        // the name
        "getDefaultDevice",
        // the implementation
        []() -> error_t::device_type {
            // my index knows
            return error_t::index().device();
        },
        // the docstring
        "get the default device of all error channels");

    // install a new default device
    cls.def_static(
        // the name
        "setDefaultDevice",
        // the implementation
        [](error_t::device_type device) -> error_t::device_type {
            // get the current setting
            auto old = error_t::index().device();
            // install the new device
            error_t::index().device(device);
            // and hand back the previous one
            return old;
        },
        // the signature
        "device"_a,
        // the docstring
        "make {device} the default device of all error channels, and return the previous one");

    // interface
    // activate
    cls.def(
        "activate",
        // the method;
        &error_t::activate,
        // the docstring
        "enable output generation");

    // deactivate
    cls.def(
        "deactivate",
        // the method
        &error_t::deactivate,
        // the docstring
        "disable output generation");

    // dent control
    cls.def(
        "indent",
        // the method;
        &error_t::indent,
        // the signature
        "levels"_a = 1,
        // the docstring
        "indent output by the indicated number of {levels}");

    cls.def(
        "outdent",
        // the method;
        &error_t::outdent,
        // the signature
        "levels"_a = 1,
        // the docstring
        "outdent output by the indicated number of {levels}");

    // add a line to the contents
    cls.def(
        "line",
        // the handler
        [](error_t & channel, const error_t::string_type & message) -> error_t & {
            // inject
            channel << message << pyre::journal::newline;
            // all done
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
        [](error_t & channel, py::iterable report) -> error_t & {
            // extract individual lines from the iterable
            for (auto line : report) {
                // and inject each one
                channel << line << pyre::journal::newline;
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
        [](error_t & channel, const error_t::string_type & message,
           // additional arguments are interpreted as entry notes
           py::kwargs kwds) -> py::object {
            // unpack {kwds}
            for (auto entry : kwds) {
                // and treat each one as a note
                channel << pyre::journal::note(py::str(entry.first), py::str(entry.second));
            }
            // inject and flush; a fatal channel raises here, otherwise it hands back the
            // exception that states the condition
            auto outcome = channel << locator() << message << pyre::journal::endl;
            // hand back its python counterpart, so the caller can raise it
            return pyre::journal::py::complaint("ApplicationError", outcome);
        },
        // the signature
        "message"_a = "",
        // the docstring
        "add the optional {message} to the channel contents and then record the entry");

    // operator bool
    cls.def(
        "__bool__",
        // the implementation
        [](const error_t & channel) -> bool {
            // interpret as a request for the activation state
            return channel.active();
        },
        // the docstring
        "syntactic sugar for checking the activation state of the channel");

    // send output to a trash can
    cls.def_static(
        "quiet",
        // the implementation
        &error_t::quiet,
        // the docstring
        "suppress all output from error channels");

    // send output to a log file
    cls.def_static(
        "logfile",
        // the implementation
        [](const error_t::string_type & path, const error_t::string_type & mode) -> void {
            // initialize the mode
            auto flag = std::ios_base::out;
            // if {mode} is {append}
            if (mode == "a") {
                // set the corresponding bit
                flag |= std::ios_base::app;
            }
            // set up the device
            error_t::logfile(path, flag);
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
