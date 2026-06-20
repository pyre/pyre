// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "Location.h"


// an hdf5 dataset
class pyre::h5::DataSet : public pyre::h5::Location {
    // types
public:
    // the class of my datatype: integer, float, string, ...
    using class_type = H5T_class_t;

    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit DataSet(id_type id);
    // the full set of special members
    DataSet(const DataSet &) = default;
    DataSet(DataSet &&) noexcept = default;
    DataSet & operator=(const DataSet &) = default;
    DataSet & operator=(DataSet &&) noexcept = default;
    ~DataSet() override = default;

    // interface
public:
    // my full path name within the file
    auto name() const -> string_t;
    // my on-disk byte offset, if contiguously stored
    auto offset() const -> haddr_t;
    // the class of my datatype
    auto cell() const -> class_type;
    // my datatype, as a fresh owned wrapper
    auto datatype() const -> types::Datatype;
    // my dataspace, as a fresh owned wrapper
    auto dataspace() const -> DataSpace;
    // my on-disk size, in bytes
    auto storageSize() const -> hsize_t;
    // my in-memory size, in bytes
    auto memorySize() const -> std::size_t;
    // my access property list, as a fresh owned wrapper
    auto dapl() const -> properties::DAPL;
    // my creation property list, as a fresh owned wrapper
    auto dcpl() const -> properties::DCPL;

    // raw value access; {memspace}/{filespace} default to the whole extent
    // fill {buffer}, interpreted as {memtype}, from the selected region
    auto read(
        id_type memtype, void * buffer, id_type memspace = H5S_ALL,
        id_type filespace = H5S_ALL) const -> void;
    // write {buffer}, interpreted as {memtype}, into the selected region
    auto write(
        id_type memtype, const void * buffer, id_type memspace = H5S_ALL,
        id_type filespace = H5S_ALL) const -> void;
    // read my contents as a string, trimming the persisted padding
    auto readString(id_type memspace = H5S_ALL, id_type filespace = H5S_ALL) const -> string_t;
    // write {value} into me as a string
    auto writeString(
        const string_t & value, id_type memspace = H5S_ALL, id_type filespace = H5S_ALL) const
        -> void;

    // release my handle
    auto close() -> void;

    // implementation details
private:
    // trim the persisted padding from {value} according to the string padding strategy {pad}
    auto _trim(string_t & value, H5T_str_t pad) const -> void;
};


// end of file
