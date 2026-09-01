// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"
// the out-of-core mosaic machinery
#include "mosaics.h"

// helpers
namespace pyre::h5::py {

    // read a tile from {self} into any writable python buffer
    // a pyre grid, a pyre memory buffer, and a numpy array all present the python buffer
    // protocol, so a single entry point serves them all; the grid family no longer needs its
    // cross product of instantiations bound here
    inline auto readInto(
        const DataSet & self, const py::buffer & data, const datatype_t & memtype,
        const shape_t & origin, const shape_t & shape) -> void
    {
        // ask the buffer for writable access to its block
        auto info = data.request(true);
        // work out how many cells the tile holds
        hsize_t cells = 1;
        for (auto extent : shape) {
            cells *= extent;
        }
        // the block has to be able to hold them
        if (static_cast<hsize_t>(info.size) < cells) {
            // if it cannot, make a channel
            auto channel = pyre::journal::error_t("pyre.h5");
            // complain
            channel
                // what
                << "the destination is too small for the tile"
                << pyre::journal::newline
                // details
                << "it holds " << info.size << " cells, and the tile has "
                << cells
                // where
                << pyre::journal::endl(__HERE__);
            // and bail, rather than let the library write past the end of somebody's array
            return;
        }
        // describe the destination with the SHAPE of the tile, rather than as a flat run of
        // the same number of cells. the two hold the same elements and the library accepts
        // either, so this looks like a matter of taste -- it is not. a destination whose
        // rank does not match the source's cannot be filled by the path that hands over a
        // whole chunk, so the library falls back to a general scatter and inflates the chunk
        // again on every read, however much of it is already sitting in the chunk cache.
        // measured against a compressed NISAR product, that is the difference between
        // repeating a read in 0.05ms and repeating it in 5ms
        auto memspace = dataspace_t(shape);
        // the source, restricted to the requested tile
        auto filespace = self.dataspace();
        filespace.slab(origin, shape);
        // fill the block; {memtype} is a pyre wrapper, so hand over its raw ids
        self.read(memtype.id(), info.ptr, memspace.id(), filespace.id());
    }

    // write the contents of any python buffer out to a tile of {self}
    inline auto writeFrom(
        const DataSet & self, const py::buffer & data, const datatype_t & memtype,
        const shape_t & origin, const shape_t & shape) -> void
    {
        // ask the buffer for read access to its block
        auto info = data.request(false);
        // the in-memory dataspace matches the tile
        auto memspace = dataspace_t(shape);
        // the destination, restricted to the requested tile
        auto filespace = self.dataspace();
        filespace.slab(origin, shape);
        // hand the block to the write
        self.write(memtype.id(), info.ptr, memspace.id(), filespace.id());
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

    // the chunk table: which of the chunks my tiling describes have actually been written
    cls.def_property_readonly(
        // the name
        "chunks",
        // the implementation
        [](const DataSet & self) -> py::object {
            // ask
            auto count = self.chunks();
            // a dataset that is not stored as chunks has no table at all
            if (!count) {
                // and says so
                return py::none();
            }
            // otherwise, hand back the tally
            return py::cast(*count);
        },
        // the docstring
        "the number of chunks i hold, or {None} when i am not stored as chunks");

    cls.def(
        // the name
        "chunk",
        // the implementation
        [](const DataSet & self, hsize_t index) -> py::object {
            // ask
            auto chunk = self.chunk(index);
            // an index that names nothing
            if (!chunk) {
                // comes back empty
                return py::none();
            }
            // otherwise, hand back the description
            return py::cast(*chunk);
        },
        // the signature
        "index"_a,
        // the docstring
        "the chunk at {index} of my table, in the logical order of chunk origins");

    cls.def(
        // the name
        "chunkAt",
        // the implementation
        [](const DataSet & self, const index_t & origin) -> py::object {
            // ask
            auto chunk = self.chunkAt(origin);
            // a chunk nobody ever wrote
            if (!chunk) {
                // comes back empty, which is how a caller learns the region is pure fill
                return py::none();
            }
            // otherwise, hand back the description
            return py::cast(*chunk);
        },
        // the signature
        "origin"_a,
        // the docstring
        "the chunk that holds the cell at {origin}, or {None} if it has never been written");

    // direct chunk access: moving a chunk in the form it is stored in, without decoding it
    cls.def(
        // the name
        "readChunk",
        // the implementation
        [](const DataSet & self, const index_t & origin) -> py::object {
            // somewhere to put the stored bytes; the dataset sizes it
            auto buffer = bytes_t();
            // pull the chunk
            auto filterMask = self.readChunk(origin, buffer);
            // a chunk that was never written has nothing to hand over
            if (!filterMask) {
                // and says so
                return py::none();
            }
            // otherwise, hand back the mask alongside the bytes, since a caller that means
            // to lay these down elsewhere needs both
            return py::make_tuple(*filterMask, py::bytes(buffer.data(), buffer.size()));
        },
        // the signature
        "origin"_a,
        // the docstring
        "the stored bytes of the chunk holding {origin}, as a {(filterMask, bytes)} pair, or "
        "{None} if it has never been written");

    cls.def(
        // the name
        "writeChunk",
        // the implementation
        [](const DataSet & self, const index_t & origin, unsigned int filterMask,
           const py::buffer & data) -> void {
            // ask the source for read access to its block
            auto info = data.request(false);
            // measure it, in bytes rather than in whatever it thinks its cells are
            auto span = static_cast<std::size_t>(info.size * info.itemsize);
            // take a copy, since the library wants a contiguous run it can hand to the file
            auto first = static_cast<const char *>(info.ptr);
            auto buffer = bytes_t(first, first + span);
            // and lay it down
            self.writeChunk(origin, filterMask, buffer);
            // all done
            return;
        },
        // the signature
        "origin"_a, "filterMask"_a, "data"_a,
        // the docstring
        "lay {data}, already in stored form, down as the chunk that holds {origin}");

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
    // the value that stands in for cells nobody wrote
    cls.def_property_readonly(
        // the name
        "fillValue",
        // the implementation, which reads my own type rather than being told one, so the
        // question cannot be asked the wrong way
        [](const DataSet & self) -> py::object {
            // find out what i hold
            auto type = self.cell();
            // integers come back as integers
            if (type == H5T_INTEGER) {
                // ask for it in those terms
                auto value = self.fillValue<std::int64_t>();
                // and lift it into python, or nothing if i was made without one
                return value ? py::cast(*value) : py::none();
            }
            // reals as reals
            if (type == H5T_FLOAT) {
                // ask for it in those terms
                auto value = self.fillValue<double>();
                // and lift it
                return value ? py::cast(*value) : py::none();
            }
            // a compound of two reals is how a complex number reaches the file
            if (type == H5T_COMPOUND) {
                // ask for it in those terms
                auto value = self.fillValue<std::complex<double>>();
                // and lift it
                return value ? py::cast(*value) : py::none();
            }
            // anything else has no python spelling yet
            return py::none();
        },
        // the docstring
        "the value that stands in for my cells nobody wrote, or {None} when i was made "
        "without one");

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

    // reading and writing, over the universal python buffer protocol
    cls.def(
        // the name
        "read",
        // the implementation
        &readInto,
        // the signature
        "data"_a, "memtype"_a, "origin"_a, "shape"_a,
        // the docstring
        "fill {data} with the tile @{origin}+{shape}");
    cls.def(
        // the name
        "write",
        // the implementation
        &writeFrom,
        // the signature
        "data"_a, "memtype"_a, "origin"_a, "shape"_a,
        // the docstring
        "write {data} to the tile @{origin}+{shape}");

    // the out-of-core mosaic factories
    bindMosaics(cls);

    // all done
    return;
}


// end of file
