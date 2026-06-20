// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "DataSet.h"
// the wrappers i hand back
#include "types/Datatype.h"
#include "DataSpace.h"
#include "properties/DAPL.h"
#include "properties/DCPL.h"


// adopt an existing raw handle
pyre::h5::DataSet::DataSet(id_type id) : Location(id) {}


// my full path name within the file
auto
pyre::h5::DataSet::name() const -> string_t
{
    // find out how long my name is
    auto len = H5Iget_name(id(), nullptr, 0);
    // make room for it, plus the terminating null
    string_t buffer(len + 1, '\0');
    // retrieve it
    H5Iget_name(id(), buffer.data(), len + 1);
    // trim the terminator and report
    buffer.resize(len);
    return buffer;
}


// my on-disk byte offset, if contiguously stored
auto
pyre::h5::DataSet::offset() const -> haddr_t
{
    // ask the library
    return H5Dget_offset(id());
}


// the class of my datatype
auto
pyre::h5::DataSet::cell() const -> class_type
{
    // grab my datatype
    auto type = H5Dget_type(id());
    // read its class
    auto cls = H5Tget_class(type);
    // give the temporary type back
    H5Tclose(type);
    // and report
    return cls;
}


// my datatype, as a fresh owned wrapper
auto
pyre::h5::DataSet::datatype() const -> types::Datatype
{
    // {H5Dget_type} hands back a fresh handle the wrapper adopts
    return types::Datatype(static_cast<id_type>(H5Dget_type(id())));
}


// my dataspace, as a fresh owned wrapper
auto
pyre::h5::DataSet::dataspace() const -> DataSpace
{
    // {H5Dget_space} hands back a fresh handle the wrapper adopts
    return DataSpace(static_cast<id_type>(H5Dget_space(id())));
}


// my on-disk size, in bytes
auto
pyre::h5::DataSet::storageSize() const -> hsize_t
{
    // ask the library
    return H5Dget_storage_size(id());
}


// my in-memory size, in bytes
auto
pyre::h5::DataSet::memorySize() const -> std::size_t
{
    // my number of elements comes from my dataspace
    auto space = H5Dget_space(id());
    auto points = H5Sget_simple_extent_npoints(space);
    H5Sclose(space);
    // the size of each comes from my datatype
    auto type = H5Dget_type(id());
    auto size = H5Tget_size(type);
    H5Tclose(type);
    // the total is the product
    return static_cast<std::size_t>(points) * size;
}


// my access property list, as a fresh owned wrapper
auto
pyre::h5::DataSet::dapl() const -> properties::DAPL
{
    // {H5Dget_access_plist} hands back a fresh handle the wrapper adopts
    return properties::DAPL(static_cast<id_type>(H5Dget_access_plist(id())));
}


// my creation property list, as a fresh owned wrapper
auto
pyre::h5::DataSet::dcpl() const -> properties::DCPL
{
    // {H5Dget_create_plist} hands back a fresh handle the wrapper adopts
    return properties::DCPL(static_cast<id_type>(H5Dget_create_plist(id())));
}


// fill {buffer}, interpreted as {memtype}, from the selected region
auto
pyre::h5::DataSet::read(id_type memtype, void * buffer, id_type memspace, id_type filespace) const
    -> void
{
    // hand it to the library
    H5Dread(id(), memtype, memspace, filespace, H5P_DEFAULT, buffer);
    // all done
    return;
}


// write {buffer}, interpreted as {memtype}, into the selected region
auto
pyre::h5::DataSet::write(
    id_type memtype, const void * buffer, id_type memspace, id_type filespace) const -> void
{
    // hand it to the library
    H5Dwrite(id(), memtype, memspace, filespace, H5P_DEFAULT, buffer);
    // all done
    return;
}


// read my contents as a string, trimming the persisted padding
auto
pyre::h5::DataSet::readString(id_type memspace, id_type filespace) const -> string_t
{
    // grab my datatype
    auto type = H5Dget_type(id());
    // variable length strings come back as a library-allocated pointer
    if (H5Tis_variable_str(type) > 0) {
        // make room for the pointer
        char * raw = nullptr;
        // read it
        H5Dread(id(), type, memspace, filespace, H5P_DEFAULT, &raw);
        // copy it into a managed string
        string_t value(raw ? raw : "");
        // give the library's buffer back
        H5free_memory(raw);
        // release the temporary type
        H5Tclose(type);
        // and report; variable length strings carry no padding to trim
        return value;
    }
    // fixed length strings come back inline; remember how they are padded
    auto pad = H5Tget_strpad(type);
    // make a buffer the right size
    auto size = H5Tget_size(type);
    string_t value(size, '\0');
    // read into it
    H5Dread(id(), type, memspace, filespace, H5P_DEFAULT, value.data());
    // release the temporary type
    H5Tclose(type);
    // trim the padding and report
    _trim(value, pad);
    return value;
}


// write {value} into me as a string
auto
pyre::h5::DataSet::writeString(const string_t & value, id_type memspace, id_type filespace) const
    -> void
{
    // grab my datatype
    auto type = H5Dget_type(id());
    // variable length strings go out as a pointer to the contents
    if (H5Tis_variable_str(type) > 0) {
        // the library copies from the address i hand it
        const char * raw = value.data();
        H5Dwrite(id(), type, memspace, filespace, H5P_DEFAULT, &raw);
        // release the temporary type
        H5Tclose(type);
        // all done
        return;
    }
    // fixed length strings go out inline; pad the value out to the stored size
    auto size = H5Tget_size(type);
    string_t buffer = value;
    buffer.resize(size, '\0');
    // write it
    H5Dwrite(id(), type, memspace, filespace, H5P_DEFAULT, buffer.data());
    // release the temporary type
    H5Tclose(type);
    // all done
    return;
}


// release my handle
auto
pyre::h5::DataSet::close() -> void
{
    // give up my reference; the library closes the dataset when the last one goes away
    _release();
    // all done
    return;
}


// trim the persisted padding from {value} according to the string padding strategy {pad}
auto
pyre::h5::DataSet::_trim(string_t & value, H5T_str_t pad) const -> void
{
    // deduce the terminator from the padding method
    switch (pad) {
        // null padded or null terminated strings end at the first null
        case H5T_STR_NULLPAD:
        case H5T_STR_NULLTERM: {
            // find the first null
            auto stop = value.find('\0');
            // and drop everything from there on, if any
            if (stop != string_t::npos) {
                value.resize(stop);
            }
            break;
        }
        // fortran style strings are padded on the right with spaces
        case H5T_STR_SPACEPAD: {
            // find the last non-space
            auto stop = value.find_last_not_of(' ');
            // and keep up to and including it
            value.resize(stop == string_t::npos ? 0 : stop + 1);
            break;
        }
        // anything else is a bug: hdf5 has added a method we don't know about
        default: {
            auto channel = pyre::journal::firewall_t("pyre.h5.dataset");
            channel
                // what
                << "unknown string padding method "
                << pad
                // where
                << pyre::journal::endl(__HERE__);
            break;
        }
    }
    // all done
    return;
}


// end of file
