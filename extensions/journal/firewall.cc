// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add bindings for the firewall channel
void
pyre::journal::py::firewall(py::module & m)
{
    // type aliases for the member functions (mfp: method pointer)
    // detail
    using getDetail_mfp = firewall_t::detail_type (firewall_t::*)() const;
    using setDetail_mfp = firewall_t & (firewall_t::*) (firewall_t::detail_type);
    // active
    using getActive_mfp = firewall_t::active_type (firewall_t::*)() const;
    using setActive_mfp = firewall_t & (firewall_t::*) (firewall_t::active_type);
    // fatal
    using getFatal_mfp = firewall_t::fatal_type (firewall_t::*)() const;
    using setFatal_mfp = firewall_t & (firewall_t::*) (firewall_t::fatal_type);
    // device
    using getDevice_mfp = firewall_t::device_type (firewall_t::*)() const;
    using setDevice_mfp = firewall_t & (firewall_t::*) (firewall_t::device_type);


    // the firewall channel interface
    py::class_<firewall_t>(m, "Firewall")
        // the constructor
        .def(
            // the implementation
            py::init<const firewall_t::name_type &>(),
            // the signature
            "name"_a)

        // accessors
        // the name; read-only property
        .def_property_readonly(
            "name",
            // only getter
            &firewall_t::name,
            // the docstring
            "my name")

        // the detail level
        .def_property(
            "detail",
            // the getter
            (getDetail_mfp) &firewall_t::detail,
            // the setter
            (setDetail_mfp) &firewall_t::detail,
            // the docstring
            "the detail level")

        // the channel activation state; mutable property
        .def_property(
            "active",
            // the getter
            (getActive_mfp) &firewall_t::active,
            // the setter
            (setActive_mfp) &firewall_t::active,
            // the docstring
            "the channel activation state")

        // the channel activation state; mutable property
        .def_property(
            "fatal",
            // the getter
            (getFatal_mfp) &firewall_t::fatal,
            // the setter
            (setFatal_mfp) &firewall_t::fatal,
            // the docstring
            "the channel activation state")

        // the registered device: mutable property
        .def_property(
            "device",
            // the getter
            (getDevice_mfp) &firewall_t::device,
            // the setter
            (setDevice_mfp) &firewall_t::device,
            // the docstring
            "the output device")

        // the contents of the current entry
        .def_property_readonly(
            "page",
            // the getter
            // N.B. the explicit declaration of the λ return value is
            // critical in making the page read/write in python
            [](firewall_t & channel) -> pyre::journal::page_t & {
                // get the current page
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
            [](firewall_t & channel) -> pyre::journal::notes_t & {
                // get the notes of the current page
                return channel.entry().notes();
            },
            // the docstring
            "the notes associated with the current entry")

        // access to the exception
        .def_property_readonly_static(
            "FirewallError",
            // the getter
            [m](py::object) -> py::object {
                // this is a module level attribute
                return m.attr("FirewallError");
            },
            // the docstring
            "the type of exception raised when this channel type is fatal")

        // the channel severity: static read-only property
        .def_property_readonly_static(
            "severity",
            // the getter
            [](py::object) -> firewall_t::string_type {
                // hardwired, as it is unlikely to change
                return "firewall";
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
            [](py::object) -> firewall_t::active_type {
                // my index knows
                return firewall_t::index().active();
            },
            // the docstring
            "the default state of firewall channels")

        // the default fatal state: static read-only property
        .def_property_readonly_static(
            "defaultFatal",
            // the getter
            [](py::object) -> firewall_t::fatal_type {
                // my index knows
                return firewall_t::index().fatal();
            },
            // the docstring
            "the default fatality of firewall channels")

        // the default device: static mutable property
        .def_property_static(
            "defaultDevice",
            // the getter
            [](py::object) -> firewall_t::device_type {
                // get the default device
                return firewall_t::index().device();
            },
            // the setter
            [](py::object, firewall_t::device_type device) -> void {
                // set the default device
                firewall_t::index().device(device);
                // all done
                return;
            },
            // the docstring
            "the default device for all firewall channels")

        // interface
        // activate
        .def(
            "activate",
            // the method;
            &firewall_t::activate,
            // the docstring
            "enable output generation")

        // deactivate
        .def(
            "deactivate",
            // the method
            &firewall_t::deactivate,
            // the docstring
            "disable output generation")

        // add a line to the contents
        .def(
            "line",
            // the handler
            [](firewall_t & channel, const firewall_t::string_type & message) -> firewall_t & {
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
            [](firewall_t & channel, py::iterable report) -> firewall_t & {
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
            [](firewall_t & channel, const firewall_t::string_type & message) -> firewall_t & {
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
            [](const firewall_t & channel) -> bool {
                // interpret as a request for the activation state
                return channel.active();
            },
            // the docstring
            "syntactic sugar for checking the activation state of the channel")

        // send output to a trash can
        .def_static(
            "quiet",
            // the implementation
            &firewall_t::quiet,
            // the docstring
            "suppress all output from firewalls")

        // send output to a log file
        .def_static(
            "logfile",
            // the implementation
            [](const firewall_t::string_type & path, const firewall_t::string_type & mode) -> void {
                // initialize the mode
                auto flag = std::ios_base::out;
                // if {mode} is {append}
                if (mode == "a") {
                    // set the corresponding bit
                    flag |= std::ios_base::app;
                }
                // set up the device
                firewall_t::logfile(path, flag);
                // all done
                return;
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
