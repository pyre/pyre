// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// augment the namespace
namespace pyre::journal::py::trampoline {
    // with the device trampoline
    class Bounce;
} // namespace pyre::journal::py::trampoline

class pyre::journal::py::trampoline::Bounce : public device_t {
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
    py::class_<device_t, device_t::pointer_type, trampoline::Bounce>(m, "Device")
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

    // all done
    return;
}


// end of file
