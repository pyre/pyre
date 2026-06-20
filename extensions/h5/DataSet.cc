// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// helpers
namespace pyre::h5::py {

    // bindings for reading dataset contents into {pyre::memory} buffers
    template <class memT>
    inline auto bindReadBuffer(py::class_<DataSet> & cls) -> void
    {
        // add a {read} overload for a memory buffer
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
    inline auto bindWriteBuffer(py::class_<DataSet> & cls) -> void
    {
        // add a {write} overload for a memory buffer
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
    inline auto bindReadGrid(py::class_<DataSet> & cls) -> void
    {
        // add a {read} overload for a compatible grid
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
    inline auto bindWriteGrid(py::class_<DataSet> & cls) -> void
    {
        // add a {write} overload for a compatible grid
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
        &DataSet::id,
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
        [](const DataSet & self) -> DAPL {
            // hand back my access property list as an owned pyre wrapper
            return self.dapl();
        },
        // the docstring
        "get my access property list");

    // creation property list
    cls.def_property_readonly(
        // the name
        "dcpl",
        // the implementation
        [](const DataSet & self) -> DCPL {
            // hand back my creation property list as an owned pyre wrapper
            return self.dcpl();
        },
        // the docstring
        "get my creation property list");

    // the on-disk offset
    cls.def_property_readonly(
        // the name
        "offset",
        // the implementation
        &DataSet::offset,
        // the docstring
        "get the on-disk offset of the dataset");

    // attempt to get the dataset contents as an int
    cls.def(
        // the name
        "int",
        // the implementation
        [](const DataSet & self) -> long {
            // get my type
            auto type = self.cell();
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
            self.read(H5T_NATIVE_LONG, &result);
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
            auto type = self.cell();
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
            self.write(H5T_NATIVE_LONG, &value);
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
            auto type = self.cell();
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
            self.read(H5T_NATIVE_DOUBLE, &result);
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
            auto type = self.cell();
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
            self.write(H5T_NATIVE_DOUBLE, &value);
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
            auto type = self.cell();
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
            // read my contents as a string, trimmed of the persisted padding
            return self.readString();
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
            auto type = self.cell();
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
            // write the string
            self.writeString(value);
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
            auto type = self.cell();
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
            // my dataspace tells me how many strings i hold
            auto space = self.dataspace();
            auto rank = space.rank();
            // make sure i'm a list at most
            if (rank > 1) {
                // if not, make a channel
                auto channel = pyre::journal::error_t("pyre.h5");
                // complain
                channel
                    // what
                    << "not a list "
                    // where
                    << pyre::journal::endl(__HERE__);
                // and bail with an empty list
                return strings_t();
            }
            // a rank of zero means a single string; read it, trimmed, as a one-element list
            if (rank == 0) {
                return strings_t { self.readString() };
            }
            // otherwise i hold a list; find out how long it is
            auto len = space.shape()[0];
            // make a correctly sized vector to hold the result
            auto strings = strings_t(len);
            // a one-element scratch dataspace for the in-memory side
            auto memspace = DataSpace(shape_t { 1 });
            // and my own dataspace for selecting one element at a time on disk
            auto filespace = self.dataspace();
            // pull one string at a time
            for (hsize_t idx = 0; idx < len; ++idx) {
                // restrict the read to the string at offset {idx}
                filespace.slab(index_t { idx }, shape_t { 1 });
                // read it, trimmed
                strings[idx] = self.readString(memspace.id(), filespace.id());
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
            auto type = self.cell();
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
            // my dataspace tells me how many strings i can hold
            auto dst = self.dataspace();
            auto rank = dst.rank();
            // make sure i'm a list
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
            // find out how long it is
            auto len = dst.shape()[0];
            // a one-element scratch dataspace for the in-memory side
            auto src = DataSpace(shape_t { 1 });
            // push one string at a time
            for (hsize_t idx = 0; idx < len; ++idx) {
                // pick the slot in the destination dataspace
                dst.slab(index_t { idx }, shape_t { 1 });
                // write it
                self.writeString(value[idx], src.id(), dst.id());
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
            auto type = self.cell();
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
            self.read(H5T_NATIVE_LONG, &result);
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
            auto type = self.cell();
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
            self.write(H5T_NATIVE_LONG, &value);
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
    // into 1d in-memory grids
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
    // into 2d in-memory grids
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
    // into 3d in-memory grids
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

    // into 1d on-disk grids
    bindReadGrid<int8_mapgrid_1d_t>(cls);
    bindReadGrid<int16_mapgrid_1d_t>(cls);
    bindReadGrid<int32_mapgrid_1d_t>(cls);
    bindReadGrid<int64_mapgrid_1d_t>(cls);
    bindReadGrid<uint8_mapgrid_1d_t>(cls);
    bindReadGrid<uint16_mapgrid_1d_t>(cls);
    bindReadGrid<uint32_mapgrid_1d_t>(cls);
    bindReadGrid<uint64_mapgrid_1d_t>(cls);
    bindReadGrid<float_mapgrid_1d_t>(cls);
    bindReadGrid<double_mapgrid_1d_t>(cls);
    bindReadGrid<complexfloat_mapgrid_1d_t>(cls);
    bindReadGrid<complexdouble_mapgrid_1d_t>(cls);
    // into 2d on-disk grids
    bindReadGrid<int8_mapgrid_2d_t>(cls);
    bindReadGrid<int16_mapgrid_2d_t>(cls);
    bindReadGrid<int32_mapgrid_2d_t>(cls);
    bindReadGrid<int64_mapgrid_2d_t>(cls);
    bindReadGrid<uint8_mapgrid_2d_t>(cls);
    bindReadGrid<uint16_mapgrid_2d_t>(cls);
    bindReadGrid<uint32_mapgrid_2d_t>(cls);
    bindReadGrid<uint64_mapgrid_2d_t>(cls);
    bindReadGrid<float_mapgrid_2d_t>(cls);
    bindReadGrid<double_mapgrid_2d_t>(cls);
    bindReadGrid<complexfloat_mapgrid_2d_t>(cls);
    bindReadGrid<complexdouble_mapgrid_2d_t>(cls);
    // into 3d on-disk grids
    bindReadGrid<int8_mapgrid_3d_t>(cls);
    bindReadGrid<int16_mapgrid_3d_t>(cls);
    bindReadGrid<int32_mapgrid_3d_t>(cls);
    bindReadGrid<int64_mapgrid_3d_t>(cls);
    bindReadGrid<uint8_mapgrid_3d_t>(cls);
    bindReadGrid<uint16_mapgrid_3d_t>(cls);
    bindReadGrid<uint32_mapgrid_3d_t>(cls);
    bindReadGrid<uint64_mapgrid_3d_t>(cls);
    bindReadGrid<float_mapgrid_3d_t>(cls);
    bindReadGrid<double_mapgrid_3d_t>(cls);
    bindReadGrid<complexfloat_mapgrid_3d_t>(cls);
    bindReadGrid<complexdouble_mapgrid_3d_t>(cls);

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
