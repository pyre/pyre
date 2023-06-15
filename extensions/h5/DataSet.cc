// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// helpers
namespace pyre::h5::py {

    // bindings for reading dataset contents into {pyre::memory} buffers
    template <class memT>
    auto bindReadBuffer(py::class_<DataSet> & cls) -> void
    {
        // add a {write} overload for the given grid type
        cls.def(
            // the name
            "read",
            // the implementation
            &read<memT>,
            // the signature
            "data"_a, "memtype"_a, "origin"_a, "shape"_a,
            // the docstring
            "fill {data} with the tile @{origin}+{shape}");
    }

    // bindings for writing out the contents of {pyre::memory} buffers
    template <class memT>
    auto bindWriteBuffer(py::class_<DataSet> & cls) -> void
    {
        // add a {write} overload for the given grid type
        cls.def(
            // the name
            "write",
            // the implementation
            &write<memT>,
            // the signature
            "data"_a, "memtype"_a, "origin"_a, "shape"_a,
            // the docstring
            "fill {data} with the tile @{origin}+{shape}");
    }

    // bindings for writing out the contents of grids
    template <class gridT>
    auto bindWriteGrid(py::class_<DataSet> & cls) -> void
    {
        // add a {write} overload for the given grid type
        cls.def(
            // the name
            "write",
            // the implementation
            &writeGrid<gridT>,
            // the signature
            "data"_a, "memtype"_a, "origin"_a, "shape"_a,
            // the docstring
            "fill {data} with the tile @{origin}+{shape}");
    }
} // namespace pyre::h5::py

// datasets
void
pyre::h5::py::dataset(py::module & m)
{
    // add bindings for hdf5 datasets
    auto cls = py::class_<DataSet>(
        // in scope
        m,
        // class name
        "DataSet",
        // docstring
        "an HDF5 dataset");

    // properties
    // my h5 handle
    cls.def_property_readonly(
        // the name
        "hid",
        // the implementation
        &DataSet::getId,
        // the docstring
        "get my h5 handle id");

    // the object categories
    cls.def_property_readonly_static(
        // the name
        "identifierType",
        // the implementation
        [](const py::object &) -> H5I_type_t {
            // i am a group
            return H5I_DATASET;
        },
        // the docstring
        "get my h5 identifier type");

    cls.def_property_readonly_static(
        // the name
        "objectType",
        // the implementation
        [](const py::object &) -> H5O_type_t {
            // i am a dataset
            return H5O_TYPE_DATASET;
        },
        // the docstring
        "get my h5 object type");

    // the dataset type
    cls.def_property_readonly(
        // the name
        "cell",
        // the implementation
        [](const DataSet & self) -> H5T_class_t {
            // get my type class
            return self.getTypeClass();
        },
        // the docstring
        "get my cell type");

    cls.def_property_readonly(
        // the name
        "type",
        // the implementation
        [](const DataSet & self) -> DataType * {
            // get my type class
            auto cls = self.getTypeClass();
            // deduce
            switch (cls) {
                // integers
                case H5T_INTEGER:
                    // return the integer data type descriptor
                    return new H5::IntType(self.getIntType());
                // floats
                case H5T_FLOAT:
                    // return the float data type descriptor
                    return new H5::FloatType(self.getFloatType());
                // strings
                case H5T_STRING:
                    // return the string data type descriptor
                    return new H5::StrType(self.getStrType());
                // compound types
                case H5T_COMPOUND:
                    // return the compound data type descriptor
                    return new H5::CompType(self.getCompType());
                // enum types
                case H5T_ENUM:
                    // return the enum data type descriptor
                    return new H5::EnumType(self.getEnumType());
                // variable length types
                case H5T_VLEN:
                    // return the variable length data type descriptor
                    return new H5::VarLenType(self.getVarLenType());
                // array types
                case H5T_ARRAY:
                    // return the array data type descriptor
                    return new H5::ArrayType(self.getArrayType());
                // by default
                default:
                    // grab whatever generic information is available
                    return new H5::DataType(self.getDataType());
            }
            // this should be unreachable, but just in case new paths open up
            return new H5::DataType(self.getDataType());
        },
        // the docstring
        "get detailed information about my type");

    // access property list
    cls.def_property_readonly(
        // the name
        "dapl",
        // the implementation
        &DataSet::getAccessPlist,
        // the docstring
        "get my access property list");

    // creation property list
    cls.def_property_readonly(
        // the name
        "dcpl",
        // the implementation
        &DataSet::getCreatePlist,
        // the docstring
        "get my creation property list");

    // the on-disk size
    cls.def_property_readonly(
        // the name
        "disksize",
        // the implementation
        &DataSet::getStorageSize,
        // the docstring
        "get the on-disk size of the dataset");

    // the in-memory size
    cls.def_property_readonly(
        // the name
        "memsize",
        // the implementation
        &DataSet::getInMemDataSize,
        // the docstring
        "get the in-memory size of the dataset");

    // the on-disk offset
    cls.def_property_readonly(
        // the name
        "offset",
        // the implementation
        &DataSet::getOffset,
        // the docstring
        "get the on-disk offset of the dataset");

    // the dataset shape
    cls.def_property_readonly(
        // the name
        "shape",
        // the implementation
        [](const DataSet & self) -> shape_t {
            // get my dataspace
            auto space = self.getSpace();
            // ask it for its rank
            auto rank = space.getSimpleExtentNdims();
            // make a correctly sized vector to hold the result
            shape_t shape(rank);
            // populate it
            space.getSimpleExtentDims(&shape[0], nullptr);
            // and return it
            return shape;
        },
        // the docstring
        "get the shape of the dataset");

    // the dataset space
    cls.def_property_readonly(
        // the name
        "space",
        // the implementation
        &DataSet::getSpace,
        // the docstring
        "get my dataspace");


    // attempt to get the dataset contents as an int
    cls.def(
        // the name
        "int",
        // the implementation
        [](const DataSet & self) -> long {
            // get my type
            auto type = self.getTypeClass();
            // check whether i am compatible with an integer
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
            self.read(&result, PredType::NATIVE_LONG);
            // all done
            return result;
        },
        // the docstring
        "extract my contents as an integer");

    // attempt to save the dataset contents as an int
    cls.def(
        // the name
        "int",
        // the implementation
        [](const DataSet & self, long value) -> void {
            // get my type
            auto type = self.getTypeClass();
            // check whether i am compatible with an integer
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
                return;
            }
            // write the data
            self.write(&value, PredType::NATIVE_LONG);
            // all done
            return;
        },
        // the signature
        "value"_a,
        // the docstring
        "save my contents as an integer");


    // attempt to get the dataset contents as a double
    cls.def(
        // the name
        "double",
        // the implementation
        [](const DataSet & self) -> double {
            // get my type
            auto type = self.getTypeClass();
            // check whether i am compatible with a floating point number
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
            self.read(&result, PredType::NATIVE_DOUBLE);
            // all done
            return result;
        },
        // the docstring
        "extract my contents as a double");

    // attempt to save the dataset contents as a double
    cls.def(
        // the name
        "double",
        // the implementation
        [](const DataSet & self, double value) -> void {
            // get my type
            auto type = self.getTypeClass();
            // check whether i am compatible with a floating point number
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
                return;
            }
            // write the data
            self.write(&value, PredType::NATIVE_DOUBLE);
            // all done
            return;
        },
        // the signature
        "value"_a,
        // the docstring
        "save my contents as a double");

    // attempt to get the dataset contents as a string
    cls.def(
        // the name
        "str",
        // the implementation
        [](const DataSet & self) -> string_t {
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

    // attempt to save the dataset contents as a string
    cls.def(
        // the name
        "str",
        // the implementation
        [](const DataSet & self, const string_t & value) -> void {
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
                return;
            }
            // read the data
            self.write(value, self.getStrType());
            // all done
            return;
        },
        // the signature
        "value"_a,
        // the docstring
        "save my contents as a string");


    // attempt to get the dataset contents as a list of strings
    cls.def(
        // the name
        "strings",
        // the implementation
        [](const DataSet & self) -> strings_t {
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
            // make sure i'm just a list;
            if (rank > 1) {
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
            // if the {rank} is zero, we have a single string; deal with it
            if (rank == 0) {
                // build a list of one string
                auto strings = strings_t(1);
                // read the data
                self.read(strings[0], self.getStrType());
                // and return
                return strings;
            }
            // if we get this far, we have a list of strings
            // make a correctly sized vector to hold the result
            shape_t shape(rank);
            // populate it
            space.getSimpleExtentDims(&shape[0], nullptr);
            // shape now knows how many strings there are
            auto len = shape[0];
            // use it to make a correctly sized vector
            auto strings = strings_t(len);
            // make a slot
            const hsize_t one = 1;
            // we always write one string at offset zero
            auto write = DataSpace(1, &one);
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

    // attempt to save the dataset contents as a list of strings
    cls.def(
        // the name
        "strings",
        // the implementation
        [](const DataSet & self, const strings_t & value) -> void {
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
                // and bail
                return;
            }
            // we have strings; let's find out how many
            // get my data space
            auto dst = self.getSpace();
            // ask it for its rank
            auto rank = dst.getSimpleExtentNdims();
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
                // and bail
                return;
            }

            // make a correctly sized vector to hold the result
            shape_t shape(rank);
            // populate it
            dst.getSimpleExtentDims(&shape[0], nullptr);

            // shape now knows how many strings this dataset can hold
            auto len = shape[0];
            // we always write one string at a time from {value}
            const hsize_t one = 1;
            // so make a data space that reflects that
            auto src = DataSpace(rank, &one);

            // write as many times as there are strings to pull
            for (hsize_t idx = 0; idx < len; ++idx) {
                // pick the slot in the destination data space
                dst.selectHyperslab(H5S_SELECT_SET, &one, &idx, nullptr, &one);
                // unconditional/unrestricted write
                self.write(value[idx], self.getStrType(), src, dst);
            }

            // all done
            return;
        },
        // the signature
        "value"_a,
        // the docstring
        "save my contents as a list of strings");


    // close the dataset
    cls.def(
        // the name
        "close",
        // the implementation
        &DataSet::close,
        // the docstring
        "close the dataset");

    // reading
    // into memory buffers
    bindReadBuffer<heap_int8_t>(cls);
    bindReadBuffer<heap_int16_t>(cls);
    bindReadBuffer<heap_int32_t>(cls);
    bindReadBuffer<heap_int64_t>(cls);
    bindReadBuffer<heap_uint8_t>(cls);
    bindReadBuffer<heap_uint16_t>(cls);
    bindReadBuffer<heap_uint32_t>(cls);
    bindReadBuffer<heap_uint64_t>(cls);
    bindReadBuffer<heap_float_t>(cls);
    bindReadBuffer<heap_double_t>(cls);
    bindReadBuffer<heap_complexfloat_t>(cls);
    bindReadBuffer<heap_complexdouble_t>(cls);

    // writing
    // from memory buffers
    bindWriteBuffer<heap_int8_t>(cls);
    bindWriteBuffer<heap_int16_t>(cls);
    bindWriteBuffer<heap_int32_t>(cls);
    bindWriteBuffer<heap_int64_t>(cls);
    bindWriteBuffer<heap_uint8_t>(cls);
    bindWriteBuffer<heap_uint16_t>(cls);
    bindWriteBuffer<heap_uint32_t>(cls);
    bindWriteBuffer<heap_uint64_t>(cls);
    bindWriteBuffer<heap_float_t>(cls);
    bindWriteBuffer<heap_double_t>(cls);
    bindWriteBuffer<heap_complexfloat_t>(cls);
    bindWriteBuffer<heap_complexdouble_t>(cls);
    // from 2d grids
    bindWriteGrid<int8_heapgrid_2d_t>(cls);
    bindWriteGrid<int16_heapgrid_2d_t>(cls);
    bindWriteGrid<int32_heapgrid_2d_t>(cls);
    bindWriteGrid<int64_heapgrid_2d_t>(cls);
    bindWriteGrid<uint8_heapgrid_2d_t>(cls);
    bindWriteGrid<uint16_heapgrid_2d_t>(cls);
    bindWriteGrid<uint32_heapgrid_2d_t>(cls);
    bindWriteGrid<uint64_heapgrid_2d_t>(cls);
    bindWriteGrid<float_heapgrid_2d_t>(cls);
    bindWriteGrid<double_heapgrid_2d_t>(cls);
    bindWriteGrid<complexfloat_heapgrid_2d_t>(cls);
    bindWriteGrid<complexdouble_heapgrid_2d_t>(cls);

    // all done
    return;
}


// end of file
