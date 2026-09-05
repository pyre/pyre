// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// augment the namespace
namespace pyre::journal::py::trampoline {
    // with the device trampoline
    class Device;
} // namespace pyre::journal::py::trampoline

class pyre::journal::py::trampoline::Device : public device_t {
    // pull the constructors
public:
    using device_t::Device;

    // interface
public:
    auto alert(const entry_t & entry) -> device_t & override
    {
        // the magic
        PYBIND11_OVERRIDE_PURE(device_t &, device_t, alert, std::ref(entry));
    };

    auto help(const entry_t & entry) -> device_t & override
    {
        // the magic
        PYBIND11_OVERRIDE_PURE(device_t &, device_t, help, std::ref(entry));
    };

    auto memo(const entry_t & entry) -> device_t & override
    {
        // the magic
        PYBIND11_OVERRIDE_PURE(device_t &, device_t, memo, std::ref(entry));
    };
};


// add bindings to the inventory
void
pyre::journal::py::devices(py::module & m)
{
    // the base device
    py::class_<device_t, device_t::pointer_type, trampoline::Device>(m, "Device")
        // constructor
        .def(py::init<string_t>(), "name"_a)
        // accessor
        .def_property_readonly("name", &device_t::name, "the name of the device")
        // the interface
        .def("alert", &device_t::alert, "entry"_a)
        .def("help", &device_t::help, "entry"_a)
        .def("memo", &device_t::memo, "entry"_a)
        // done
        ;

    // the trash can
    py::class_<trash_t, device_t, trash_t::pointer_type>(m, "Trash")
        // constructor
        .def(py::init<>())
        // done
        ;

    // the streams
    py::class_<stream_t, stream_t::pointer_type, device_t>(m, "Stream")
        // constructor
        .def(py::init<const stream_t::name_type &, stream_t::stream_type &>())
        // done
        ;

    // cout
    py::class_<cout_t, cout_t::pointer_type, stream_t>(m, "Console")
        // constructor
        .def(py::init<>())
        // done
        ;

    // cerr
    py::class_<cerr_t, cerr_t::pointer_type, stream_t>(m, "ErrorConsole")
        // constructor
        .def(py::init<>())
        // done
        ;

    // files
    py::class_<file_t, file_t::pointer_type, device_t>(m, "File")
        // constructor
        .def(
            // the implementation
            py::init<const file_t::path_type &>(),
            // the signature
            "path"_a /*, "mode"_a = "w" */)
        // done
        ;

    // couriers
    py::class_<courier_t, courier_t::pointer_type, device_t>(m, "Courier")
        // constructor
        .def(
            // the implementation
            py::init<
                courier_t::descriptor_type, const courier_t::name_type &, device_t::pointer_type>(),
            // the signature
            "descriptor"_a, "name"_a = "courier", "mirror"_a = nullptr,
            // the docstring
            "a device that ships entries as records down {descriptor}, and to {mirror}")

        // the descriptor
        .def_property_readonly(
            "descriptor",
            // the getter
            &courier_t::descriptor,
            // the docstring
            "the descriptor the records are written to")

        // the sequence number
        .def_property_readonly(
            "seq",
            // the getter
            &courier_t::seq,
            // the docstring
            "the sequence number of the last record stamped")

        // the number of records delivered
        .def_property_readonly(
            "shipped",
            // the getter
            &courier_t::shipped,
            // the docstring
            "the number of records that made it out")

        // the number of records lost
        .def_property_readonly(
            "dropped",
            // the getter
            &courier_t::dropped,
            // the docstring
            "the number of records lost since the last successful write")

        // the state of the far end
        .def_property_readonly(
            "dead",
            // the getter
            &courier_t::dead,
            // the docstring
            "whether the far end has gone away")

        // release the descriptor
        .def(
            // the name
            "close",
            // the implementation
            &courier_t::close,
            // the docstring
            "release the descriptor; nothing is delivered after this")
        // done
        ;

    // all done
    return;
}


// end of file
