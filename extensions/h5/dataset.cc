// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// datasets
void
h5::py::dataset(py::module & m)
{
    // add bindings for hdf5 datasets
    auto cls = py::class_<Dataset>(
        // in scope
        m,
        // class name
        "Dataset",
        // docstring
        "an HDF5 dataset");


    // the dataset type
    cls.def_property_readonly(
        // the name
        "cell",
        // the implementation
        [](const Dataset & self) {
            // get my type class
            return self.getTypeClass();
        },
        // the docstring
        "get the dataset cell type");


    // the dataset shape
    cls.def_property_readonly(
        // the name
        "shape",
        // the implementation
        [](const Dataset & self) -> dims_t {
            // get my dataspace
            auto space = self.getSpace();
            // ask it for its rank
            auto rank = space.getSimpleExtentNdims();
            // make a correctly sized vector to hold the result
            dims_t shape(rank);
            // populate it
            space.getSimpleExtentDims(&shape[0], nullptr);
            // and return it
            return shape;
        },
        // the docstring
        "get the shape of the dataset");


    // attempt to get the dataset contents as an int
    cls.def(
        // the name
        "int",
        // the implementation
        [](const Dataset & self) -> long {
            // get my type
            auto type = self.getTypeClass();
            // check whether i can be converted to an integer
            if (type != H5T_INTEGER) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "the dataset does not contain an integer"
                    // where
                    << pyre::journal::endl(__HERE__);
                // and bail
                return 0;
            }

            // make some room
            long result;
            // read the data
            self.read(&result, self.getIntType());

            // all done
            return result;
        },
        // the docstring
        "extract my contents as an integer");


    // attempt to get the dataset contents as a double
    cls.def(
        // the name
        "double",
        // the implementation
        [](const Dataset & self) -> double {
            // get my type
            auto type = self.getTypeClass();
            // check whether i can be converted to a floating point number
            if (type != H5T_FLOAT) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "the dataset does not contain a floating point number"
                    // where
                    << pyre::journal::endl(__HERE__);
                // and bail
                return 0;
            }

            // make some room
            double result;
            // read the data
            self.read(&result, self.getFloatType());

            // all done
            return result;
        },
        // the docstring
        "extract my contents as a double");


    // attempt to get the dataset contents as a string
    cls.def(
        // the name
        "str",
        // the implementation
        [](const Dataset & self) -> string_t {
            // get my type
            auto type = self.getTypeClass();
            // check whether i can be converted to a string
            if (type != H5T_STRING) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "the dataset does not contain a string"
                    // where
                    << pyre::journal::endl(__HERE__);
                // and bail
                return "";
            }

            // make some room
            string_t result;
            // read the data
            self.read(result, self.getStrType());

            // all done
            return result;
        },
        // the docstring
        "extract my contents as a string");


    // attempt to get the dataset contents as a list of ints
    cls.def(
        // the name
        "ints",
        // the implementation
        [](const Dataset & self) -> ints_t {
            // get my type
            auto type = self.getTypeClass();
            // check whether i contain integers
            if (type != H5T_INTEGER) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "not a dataset with integers"
                    // where
                    << pyre::journal::endl(__HERE__);
                // build an empty list of integers
                ints_t ints;
                // and bail
                return ints;
            }

            // we have ints; let's find out how many
            // get my data space
            auto space = self.getSpace();
            // ask it for its rank
            auto rank = space.getSimpleExtentNdims();
            // make a correctly sized vector to hold the result
            dims_t shape(rank);
            // populate it
            space.getSimpleExtentDims(&shape[0], nullptr);

            // make sure i'm just a list
            if (rank != 1) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "not a list "
                    // where
                    << pyre::journal::endl(__HERE__);
                // build an empty list of ints
                ints_t ints;
                // and bail
                return ints;
            }

            // shape now knows how many integers there are
            auto len = shape[0];
            // use it to make a correctly sized vector
            auto ints = ints_t(len);

            // unconditional/unrestricted read
            self.read(&ints[0], self.getIntType());

            // all done
            return ints;
        },
        // the docstring
        "get my contents as a list of ints");


    // attempt to get the dataset contents as a list of doubles
    cls.def(
        // the name
        "doubles",
        // the implementation
        [](const Dataset & self) -> doubles_t {
            // get my type
            auto type = self.getTypeClass();
            // check whether i contain doubles
            if (type != H5T_FLOAT) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "not a dataset with doubles"
                    // where
                    << pyre::journal::endl(__HERE__);
                // build an empty list of doubles
                doubles_t doubles;
                // and bail
                return doubles;
            }

            // we have doubles; let's find out how many
            // get my data space
            auto space = self.getSpace();
            // ask it for its rank
            auto rank = space.getSimpleExtentNdims();
            // make a correctly sized vector to hold the result
            dims_t shape(rank);
            // populate it
            space.getSimpleExtentDims(&shape[0], nullptr);

            // make sure i'm just a list
            if (rank != 1) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "not a list "
                    // where
                    << pyre::journal::endl(__HERE__);
                // build an empty list of doubles
                doubles_t doubles;
                // and bail
                return doubles;
            }

            // shape now knows how many doubles there are
            auto len = shape[0];
            // use it to make a correctly sized vector
            auto doubles = doubles_t(len);

            // unconditional/unrestricted read
            self.read(&doubles[0], self.getFloatType());

            // all done
            return doubles;
        },
        // the docstring
        "get my contents as a list of ints");


    // attempt to get the dataset contents as a list of strings
    cls.def(
        // the name
        "strings",
        // the implementation
        [](const Dataset & self) -> strings_t {
            // get my type
            auto type = self.getTypeClass();
            // check whether i can be converted to a list of strings
            if (type != H5T_STRING) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "not a dataset with null terminated strings"
                    // where
                    << pyre::journal::endl(__HERE__);
                // build an empty list of strings
                strings_t strings;
                // and bail
                return strings;
            }

            // we have strings; let's find out how many
            // get my data space
            auto space = self.getSpace();
            // ask it for its rank
            auto rank = space.getSimpleExtentNdims();
            // make a correctly sized vector to hold the result
            dims_t shape(rank);
            // populate it
            space.getSimpleExtentDims(&shape[0], nullptr);

            // make sure i'm just a list
            if (rank != 1) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.hdf5");
                // complain
                channel
                    // what
                    << "not a list "
                    // where
                    << pyre::journal::endl(__HERE__);
                // build an empty list of strings
                strings_t strings;
                // and bail
                return strings;
            }

            // shape now knows how many strings there are
            auto len = shape[0];
            // use it to make a correctly sized vector
            auto strings = strings_t(len);

            // make a slot
            const hsize_t one = 1;
            // we always write one string at offset zero
            auto write = Dataspace(1, &one);
            // and read from the dataset space
            auto read = self.getSpace();

            // read as many times as there are strings to pull
            for (hsize_t idx = 0; idx < len; ++idx) {
                // restrict the read dataspace to one string at offset {idx}
                read.selectHyperslab(H5S_SELECT_SET, &one, &idx);
                // unconditional/unrestricted read
                self.read(strings[idx], self.getStrType(), write, read);
            }

            // all done
            return strings;
        },
        // the docstring
        "get my contents as a list of strings");


    // all done
    return;
}


// end of file
