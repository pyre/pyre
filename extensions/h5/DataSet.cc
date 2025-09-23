// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


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
            "write the contents of {data} to the tile @{origin}+{shape}");
    }

    // bindings for reading dataset contents into {pyre::grid} buffers
    template <class gridT>
    auto bindReadGrid(py::class_<DataSet> & cls) -> void
    {
        // add a {write} overload for the given grid type
        cls.def(
            // the name
            "read",
            // the implementation
            &readGrid<gridT>,
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
            "write the contents of {data} to the tile @{origin}+{shape}");
    }

    auto trim(const DataSet & self, string_t & result) -> string_t
    {
        // to trim the possible padding, get my actual datatype descriptor
        auto strtype = self.getStrType();
        // deduce the termination method
        auto method = strtype.getStrpad();
        // use it to figure out what the terminator looks like
        switch (method) {
            // null padded or null terminated string
            case H5T_STR_NULLPAD:
            case H5T_STR_NULLTERM:
                // these are handled the same way: find the first null and trim the string
                for (auto here = result.cbegin(); here != result.cend(); ++here) {
                    // if this is not the terminator
                    if (*here != '\0') {
                        // move on
                        continue;
                    }
                    // otherwise, trim
                    result.erase(here, result.end());
                    // and bail
                    break;
                }
                // and done
                break;
            // fortran style padded strings
            case H5T_STR_SPACEPAD:
                // search from the end for the first non-space
                for (auto here = result.cend() - 1; here != result.cbegin(); --here) {
                    // this is still the padding character
                    if (*here == ' ') {
                        // move one
                        continue;
                    }
                    // otherwise, trim
                    result.erase(++here, result.cend());
                    // and bail
                    break;
                }
                // and done
                break;
            // everything else
            default: {
                // is a bug: hdf5 has added another method we don't know about
                auto channel = pyre::journal::firewall_t("pyre.h5");
                // complain
                channel
                    // what
                    << "unknown string padding method "
                    << method
                    // where
                    << pyre::journal::endl(__HERE__);
                // send it off anyway, in case firewalls aren't fatal
                break;
            }
        }
        // all done
        return result;
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

    // the on-disk offset
    cls.def_property_readonly(
        // the name
        "offset",
        // the implementation
        &DataSet::getOffset,
        // the docstring
        "get the on-disk offset of the dataset");

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
                auto channel = pyre::journal::error_t("pyre.h5");
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
                auto channel = pyre::journal::error_t("pyre.h5");
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
                auto channel = pyre::journal::error_t("pyre.h5");
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
                auto channel = pyre::journal::error_t("pyre.h5");
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
                auto channel = pyre::journal::error_t("pyre.h5");
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
            return trim(self, result);
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
                auto channel = pyre::journal::error_t("pyre.h5");
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
                auto channel = pyre::journal::error_t("pyre.h5");
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
            // make sure i'm just a list
            if (rank > 1) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.h5");
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
                // make some room
                string_t result;
                // read the data
                self.read(result, self.getStrType());
                // build a list of one string
                auto strings = strings_t(1);
                // trim and assign
                strings[0] = trim(self, result);
                // all done
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
                // make some room
                string_t result;
                // unconditional/unrestricted read
                self.read(result, self.getStrType(), write, read);
                // trim and assign
                strings[idx] = trim(self, result);
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
                auto channel = pyre::journal::error_t("pyre.h5");
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
                auto channel = pyre::journal::error_t("pyre.h5");
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

    // attempt to read the contents of the dataset as an enum
    cls.def(
        // the name
        "enum",
        // the implementation
        [](const DataSet & self) -> long {
            // get my type
            auto type = self.getTypeClass();
            // check whether i am an enumeration
            if (type != H5T_ENUM) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.h5");
                // complain
                channel
                    // what
                    << "the dataset does not contain an enumeration"
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
        "read an enum");

    // attempt to save the contents of the dataset as an enum
    cls.def(
        // the name
        "enum",
        // the implementation
        [](const DataSet & self, long value) -> void {
            // get my type
            auto type = self.getTypeClass();
            // check whether i am an enumeration
            if (type != H5T_ENUM) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.h5");
                // complain
                channel
                    // what
                    << "the dataset does not contain an enumeration"
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
        "value",
        // the docstring
        "read an enum");


    // close the dataset
    cls.def(
        // the name
        "close",
        // the implementation
        &DataSet::close,
        // the docstring
        "close the dataset");

    // access to the dataset value
    data(cls);
    // access to the dataset attributes
    attributes(cls);

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
    // into 1d grids
    bindReadGrid<int8_heapgrid_1d_t>(cls);
    bindReadGrid<int16_heapgrid_1d_t>(cls);
    bindReadGrid<int32_heapgrid_1d_t>(cls);
    bindReadGrid<int64_heapgrid_1d_t>(cls);
    bindReadGrid<uint8_heapgrid_1d_t>(cls);
    bindReadGrid<uint16_heapgrid_1d_t>(cls);
    bindReadGrid<uint32_heapgrid_1d_t>(cls);
    bindReadGrid<uint64_heapgrid_1d_t>(cls);
    bindReadGrid<float_heapgrid_1d_t>(cls);
    bindReadGrid<double_heapgrid_1d_t>(cls);
    bindReadGrid<complexfloat_heapgrid_1d_t>(cls);
    bindReadGrid<complexdouble_heapgrid_1d_t>(cls);
    // into 2d grids
    bindReadGrid<int8_heapgrid_2d_t>(cls);
    bindReadGrid<int16_heapgrid_2d_t>(cls);
    bindReadGrid<int32_heapgrid_2d_t>(cls);
    bindReadGrid<int64_heapgrid_2d_t>(cls);
    bindReadGrid<uint8_heapgrid_2d_t>(cls);
    bindReadGrid<uint16_heapgrid_2d_t>(cls);
    bindReadGrid<uint32_heapgrid_2d_t>(cls);
    bindReadGrid<uint64_heapgrid_2d_t>(cls);
    bindReadGrid<float_heapgrid_2d_t>(cls);
    bindReadGrid<double_heapgrid_2d_t>(cls);
    bindReadGrid<complexfloat_heapgrid_2d_t>(cls);
    bindReadGrid<complexdouble_heapgrid_2d_t>(cls);
    // into 3d grids
    bindReadGrid<int8_heapgrid_3d_t>(cls);
    bindReadGrid<int16_heapgrid_3d_t>(cls);
    bindReadGrid<int32_heapgrid_3d_t>(cls);
    bindReadGrid<int64_heapgrid_3d_t>(cls);
    bindReadGrid<uint8_heapgrid_3d_t>(cls);
    bindReadGrid<uint16_heapgrid_3d_t>(cls);
    bindReadGrid<uint32_heapgrid_3d_t>(cls);
    bindReadGrid<uint64_heapgrid_3d_t>(cls);
    bindReadGrid<float_heapgrid_3d_t>(cls);
    bindReadGrid<double_heapgrid_3d_t>(cls);
    bindReadGrid<complexfloat_heapgrid_3d_t>(cls);
    bindReadGrid<complexdouble_heapgrid_3d_t>(cls);

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
    // from 3d grids
    bindWriteGrid<int8_heapgrid_3d_t>(cls);
    bindWriteGrid<int16_heapgrid_3d_t>(cls);
    bindWriteGrid<int32_heapgrid_3d_t>(cls);
    bindWriteGrid<int64_heapgrid_3d_t>(cls);
    bindWriteGrid<uint8_heapgrid_3d_t>(cls);
    bindWriteGrid<uint16_heapgrid_3d_t>(cls);
    bindWriteGrid<uint32_heapgrid_3d_t>(cls);
    bindWriteGrid<uint64_heapgrid_3d_t>(cls);
    bindWriteGrid<float_heapgrid_3d_t>(cls);
    bindWriteGrid<double_heapgrid_3d_t>(cls);
    bindWriteGrid<complexfloat_heapgrid_3d_t>(cls);
    bindWriteGrid<complexdouble_heapgrid_3d_t>(cls);

    // all done
    return;
}


// end of file
