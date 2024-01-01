// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


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
            return self.getName();
        },
        // the docstring
        "get my name");

    // retrieve my h5 handle
    cls.def_property_readonly(
        // the name
        "hid",
        // the implementation
        &Attribute::getId,
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
            auto type = self.getTypeClass();
            // check whether i am compatible with an integer
            if (type != H5T_INTEGER) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "the attribute value cannot be represented as an 'int'"
                    // where
                    << pyre::journal::endl(__HERE__);
                // and bail
                return 0;
            }
            // make some room
            long result;
            // read the data
            self.read(PredType::NATIVE_LONG, &result);
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
            auto type = self.getTypeClass();
            // check whether i am compatible with an integer
            if (type != H5T_INTEGER) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "the attribute value must be representable as an 'int'"
                    // where
                    << pyre::journal::endl(__HERE__);
                // and bail
                return;
            }
            // write the data
            self.write(PredType::NATIVE_LONG, &value);
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
            auto type = self.getTypeClass();
            // check whether i am compatible with a floating point number
            if (type != H5T_FLOAT) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "the attribute value cannot be represented as a 'float'"
                    // where
                    << pyre::journal::endl(__HERE__);
                // and bail
                return 0;
            }
            // make some room
            double result;
            // read the data
            self.read(PredType::NATIVE_DOUBLE, &result);
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
            auto type = self.getTypeClass();
            // check whether i am compatible with a floating point number
            if (type != H5T_FLOAT) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "the attribute value must be representable as a 'float'"
                    // where
                    << pyre::journal::endl(__HERE__);
                // and bail
                return;
            }
            // write the data
            self.write(PredType::NATIVE_DOUBLE, &value);
            // all done
            return;
        },
        // the signature
        "value"_a,
        // the docstring
        "save my contents as a double");

    // attempt to get the attribute value as a string
    cls.def(
        // the name
        "str",
        // the implementation
        [](const Attribute & self) -> string_t {
            // get my type
            auto type = self.getTypeClass();
            // check whether i can be converted to a string
            if (type != H5T_STRING) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "the attribute value cannot be represented as a 'str'"
                    // where
                    << pyre::journal::endl(__HERE__);
                // and bail
                return "";
            }
            // make some room
            string_t result;
            // read the data
            self.read(self.getStrType(), result);
            // all done
            return result;
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
            auto type = self.getTypeClass();
            // check whether i can be converted to a string
            if (type != H5T_STRING) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "the attribute value must be representable as a 'str'"
                    // where
                    << pyre::journal::endl(__HERE__);
                // and bail
                return;
            }
            // read the data
            self.write(self.getStrType(), value);
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