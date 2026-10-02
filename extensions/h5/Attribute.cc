// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// helpers
namespace pyre::h5::py {
    // check that {self} holds a single value, and complain on behalf of an accessor that
    // treats it as a {what} if it does not
    inline auto single(const Attribute & self, const char * what) -> bool
    {
        // the number of values i hold
        auto cells = self.dataspace().cells();
        // a single one is what the scalar accessors can handle
        if (cells == 1) {
            // so all is well
            return true;
        }
        // otherwise, make a channel
        auto channel = pyre::journal::error_t("pyre.hdf5");
        // complain
        channel
            // where
            << pyre::journal::at()
            // what
            << "the attribute '" << self.name() << "' holds " << cells << " values, not a single '"
            << what
            << "'"
            // flush
            << pyre::journal::endl;
        // and refuse
        return false;
    }

    // check whether the class {type} holds complex numbers: a compound of two reals is how they
    // reached the file before hdf5 2.0 gave them a class of their own, and how most files that
    // are in use today still hold them
    inline auto isComplex(H5T_class_t type) -> bool
    {
#if H5_VERSION_GE(2, 0, 0)
        // the native class
        if (type == H5T_COMPLEX) {
            // is complex
            return true;
        }
#endif
        // and so is the compound
        return type == H5T_COMPOUND;
    }

    // read the values of {self}, which holds complex numbers, into the {std::complex<double>}
    // at {buffer}
    inline auto readComplex(const Attribute & self, void * buffer) -> void
    {
#if H5_VERSION_GE(2, 0, 0)
        // the native class
        if (self.cell() == H5T_COMPLEX) {
            // converts to the native complex, which is laid out as {std::complex<double>}
            self.read(H5T_NATIVE_DOUBLE_COMPLEX, buffer);
            // and that is all
            return;
        }
#endif
        // a compound converts to the compound of two doubles, with the library matching the
        // parts by name
        self.read(pyre::h5::datatype<std::complex<double>>().id(), buffer);
        // all done
        return;
    }

    // write the {std::complex<double>} at {buffer} into {self}, which holds complex numbers
    inline auto writeComplex(const Attribute & self, const void * buffer) -> void
    {
#if H5_VERSION_GE(2, 0, 0)
        // the native class
        if (self.cell() == H5T_COMPLEX) {
            // converts from the native complex
            self.write(H5T_NATIVE_DOUBLE_COMPLEX, buffer);
            // and that is all
            return;
        }
#endif
        // a compound converts from the compound of two doubles
        self.write(pyre::h5::datatype<std::complex<double>>().id(), buffer);
        // all done
        return;
    }

    // read all the values of {self} as {valueT}, and lift them into python: a single value as
    // itself, and anything else as a list
    template <class valueT>
    inline auto lift(const Attribute & self) -> py::object
    {
        // the number of values i hold
        auto cells = static_cast<std::size_t>(self.dataspace().cells());
        // make room for them
        auto values = std::vector<valueT>(cells);
        // complex numbers
        if constexpr (std::is_same_v<valueT, std::complex<double>>) {
            // take the path that knows both of their representations
            readComplex(self, values.data());
        } else {
            // everything else is converted by the library into the terms of {valueT}
            self.read(pyre::h5::datatype<valueT>().id(), values.data());
        }
        // a single value
        if (cells == 1) {
            // travels as itself
            return py::cast(values.front());
        }
        // anything else as a list
        return py::cast(values);
    }
} // namespace pyre::h5::py


// attributes
void
pyre::h5::py::attribute(py::module & m)
{
    // add bindings for hdf5 attributes
    auto cls = py::class_<Attribute>(
        // in scope
        m,
        // class name
        "Attribute",
        // docstring
        "an HDF5 attribute");

    // retrieve my name
    cls.def_property_readonly(
        // the name
        "name",
        // the implementation
        [](const Attribute & self) {
            // retrieve the name and return it
            return self.name();
        },
        // the docstring
        "get my name");

    // retrieve my h5 handle
    cls.def_property_readonly(
        // the name
        "hid",
        // the implementation
        &Attribute::id,
        // the docstring
        "get my h5 handle id");

    // retrieve my identifier type
    cls.def_property_readonly_static(
        // the name
        "identifierType",
        // the implementation
        [](const py::object &) -> H5I_type_t {
            // i am an attribute
            return H5I_ATTR;
        },
        // the docstring
        "get my h5 identifier type");

    // attempt to get the attribute value as an int
    cls.def(
        // the name
        "int",
        // the implementation
        [](const Attribute & self) -> long {
            // get my type
            auto type = self.cell();
            // check whether i am compatible with an integer
            if (type != H5T_INTEGER) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // where
                    << pyre::journal::at()
                    // what
                    << "the attribute value cannot be represented as an 'int'"
                    // flush
                    << pyre::journal::endl;
                // and bail
                return 0;
            }
            // and that i hold a single one
            if (!single(self, "int")) {
                // or bail
                return 0;
            }
            // make some room
            long result;
            // read the data
            self.read(H5T_NATIVE_LONG, &result);
            // all done
            return result;
        },
        // the docstring
        "extract my value as an integer");

    // attempt to save the attribute value as an int
    cls.def(
        // the name
        "int",
        // the implementation
        [](const Attribute & self, long value) -> void {
            // get my type
            auto type = self.cell();
            // check whether i am compatible with an integer
            if (type != H5T_INTEGER) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // where
                    << pyre::journal::at()
                    // what
                    << "the attribute value must be representable as an 'int'"
                    // flush
                    << pyre::journal::endl;
                // and bail
                return;
            }
            // and that i hold a single one
            if (!single(self, "int")) {
                // or bail
                return;
            }
            // write the data
            self.write(H5T_NATIVE_LONG, &value);
            // all done
            return;
        },
        // the signature
        "value"_a,
        // the docstring
        "save my contents as an integer");

    // attempt to get the attribute value as a double
    cls.def(
        // the name
        "double",
        // the implementation
        [](const Attribute & self) -> double {
            // get my type
            auto type = self.cell();
            // check whether i am compatible with a floating point number
            if (type != H5T_FLOAT) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // where
                    << pyre::journal::at()
                    // what
                    << "the attribute value cannot be represented as a 'float'"
                    // flush
                    << pyre::journal::endl;
                // and bail
                return 0;
            }
            // and that i hold a single one
            if (!single(self, "float")) {
                // or bail
                return 0;
            }
            // make some room
            double result;
            // read the data
            self.read(H5T_NATIVE_DOUBLE, &result);
            // all done
            return result;
        },
        // the docstring
        "extract my contents as a double");

    // attempt to save the attribute value as a double
    cls.def(
        // the name
        "double",
        // the implementation
        [](const Attribute & self, double value) -> void {
            // get my type
            auto type = self.cell();
            // check whether i am compatible with a floating point number
            if (type != H5T_FLOAT) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // where
                    << pyre::journal::at()
                    // what
                    << "the attribute value must be representable as a 'float'"
                    // flush
                    << pyre::journal::endl;
                // and bail
                return;
            }
            // and that i hold a single one
            if (!single(self, "float")) {
                // or bail
                return;
            }
            // write the data
            self.write(H5T_NATIVE_DOUBLE, &value);
            // all done
            return;
        },
        // the signature
        "value"_a,
        // the docstring
        "save my contents as a double");

    // attempt to get the attribute value as a complex number
    cls.def(
        // the name
        "complex",
        // the implementation
        [](const Attribute &
               self) -> std::
                         complex<double> {
                             // get my type
                             auto type = self.cell();
                             // check whether i hold complex numbers, in either of their
                             // representations
                             if (!isComplex(type)) {
                                 // if not, make a channel
                                 auto channel = pyre::journal::error_t("pyre.hdf5");
                                 // complain
                                 channel
                                     // where
                                     << pyre::journal::at()
                                     // what
                                     << "the attribute value cannot be represented as a 'complex'"
                                     // flush
                                     << pyre::journal::endl;
                                 // and bail
                                 return {};
                             }
                             // and that i hold a single one
                             if (!single(self, "complex")) {
                                 // or bail
                                 return {};
                             }
                             // make some room
                             std::complex<double> result;
                             // read the data
                             readComplex(self, &result);
                             // all done
                             return result;
                         },
        // the docstring
        "extract my contents as a complex number");

    // attempt to save the attribute value as a complex number
    cls.def(
        // the name
        "complex",
        // the implementation
        [](const Attribute & self, std::complex<double> value) -> void {
            // get my type
            auto type = self.cell();
            // check whether i hold complex numbers, in either of their representations
            if (!isComplex(type)) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // where
                    << pyre::journal::at()
                    // what
                    << "the attribute value must be representable as a 'complex'"
                    // flush
                    << pyre::journal::endl;
                // and bail
                return;
            }
            // and that i hold a single one
            if (!single(self, "complex")) {
                // or bail
                return;
            }
            // write the data
            writeComplex(self, &value);
            // all done
            return;
        },
        // the signature
        "value"_a,
        // the docstring
        "save my contents as a complex number");

    // my contents, in my own terms
    cls.def_property_readonly(
        // the name
        "value",
        // the implementation, which reads my own type rather than being told one, so the
        // question cannot be asked the wrong way
        [](const Attribute & self) -> py::object {
            // find out what i hold
            auto type = self.cell();
            // integers come back as integers
            if (type == H5T_INTEGER) {
                // one or many
                return lift<std::int64_t>(self);
            }
            // reals as reals
            if (type == H5T_FLOAT) {
                // one or many
                return lift<double>(self);
            }
            // complex numbers, in either of their representations, as complex numbers
            if (isComplex(type)) {
                // one or many
                return lift<std::complex<double>>(self);
            }
            // strings as strings
            if (type == H5T_STRING) {
                // read my value as a string
                return py::cast(self.readString());
            }
            // anything else has no python spelling yet
            return py::none();
        },
        // the docstring
        "my contents, as a number, a complex number, or a string, or a list of numbers when "
        "i hold more than one; {None} for anything else");

    // attempt to get the attribute value as a string
    cls.def(
        // the name
        "str",
        // the implementation
        [](const Attribute & self) -> string_t {
            // get my type
            auto type = self.cell();
            // check whether i can be converted to a string
            if (type != H5T_STRING) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // where
                    << pyre::journal::at()
                    // what
                    << "the attribute value cannot be represented as a 'str'"
                    // flush
                    << pyre::journal::endl;
                // and bail
                return "";
            }
            // read my value as a string
            return self.readString();
        },
        // the docstring
        "extract my contents as a string");

    // attempt to save the attribute value as a string
    cls.def(
        // the name
        "str",
        // the implementation
        [](const Attribute & self, const string_t & value) -> void {
            // get my type
            auto type = self.cell();
            // check whether i can be converted to a string
            if (type != H5T_STRING) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // where
                    << pyre::journal::at()
                    // what
                    << "the attribute value must be representable as a 'str'"
                    // flush
                    << pyre::journal::endl;
                // and bail
                return;
            }
            // write my value as a string
            self.writeString(value);
            // all done
            return;
        },
        // the signature
        "value"_a,
        // the docstring
        "save my contents as a string");

    // value access
    data(cls);

    // all done
    return;
}


// end of file
