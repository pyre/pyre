// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Attribute.h"
// the wrappers i hand back
#include "types/Datatype.h"
#include "DataSpace.h"


// adopt an existing raw handle
pyre::h5::Attribute::Attribute(id_type id) : Identifier(id) {}


// my name
auto
pyre::h5::Attribute::name() const -> string_t
{
    // find out how long my name is
    auto len = H5Aget_name(id(), 0, nullptr);
    // make room for it, plus the terminating null the library writes
    string_t buffer(len + 1, '\0');
    // retrieve it
    H5Aget_name(id(), len + 1, buffer.data());
    // trim the terminator and report
    buffer.resize(len);
    return buffer;
}


// the class of my datatype
auto
pyre::h5::Attribute::cell() const -> class_type
{
    // grab my datatype
    auto type = H5Aget_type(id());
    // read its class
    auto cls = H5Tget_class(type);
    // give the temporary type back
    H5Tclose(type);
    // and report
    return cls;
}


// my datatype, as a fresh owned wrapper
auto
pyre::h5::Attribute::datatype() const -> types::Datatype
{
    // {H5Aget_type} hands back a fresh handle the wrapper adopts
    return types::Datatype(static_cast<id_type>(H5Aget_type(id())));
}


// my dataspace, as a fresh owned wrapper
auto
pyre::h5::Attribute::dataspace() const -> DataSpace
{
    // {H5Aget_space} hands back a fresh handle the wrapper adopts
    return DataSpace(static_cast<id_type>(H5Aget_space(id())));
}


// my on-disk size, in bytes
auto
pyre::h5::Attribute::storageSize() const -> hsize_t
{
    // ask the library
    return H5Aget_storage_size(id());
}


// my in-memory size, in bytes
auto
pyre::h5::Attribute::memorySize() const -> std::size_t
{
    // my number of elements comes from my dataspace
    auto space = H5Aget_space(id());
    auto points = H5Sget_simple_extent_npoints(space);
    H5Sclose(space);
    // the size of each comes from my datatype
    auto type = H5Aget_type(id());
    auto size = H5Tget_size(type);
    H5Tclose(type);
    // the total is the product
    return static_cast<std::size_t>(points) * size;
}


// read my raw value, interpreted as {memtype}, into {buffer}
auto
pyre::h5::Attribute::read(id_type memtype, void * buffer) const -> void
{
    // hand it to the library
    H5Aread(id(), memtype, buffer);
    // all done
    return;
}


// write {buffer}, interpreted as {memtype}, into me
auto
pyre::h5::Attribute::write(id_type memtype, const void * buffer) const -> void
{
    // hand it to the library
    H5Awrite(id(), memtype, buffer);
    // all done
    return;
}


// read my value as a string
auto
pyre::h5::Attribute::readString() const -> string_t
{
    // grab my datatype
    auto type = H5Aget_type(id());
    // variable length strings come back as a library-allocated pointer
    if (H5Tis_variable_str(type) > 0) {
        // make room for the pointer
        char * raw = nullptr;
        // read it
        H5Aread(id(), type, &raw);
        // copy it into a managed string
        string_t value(raw ? raw : "");
        // give the library's buffer back
        H5free_memory(raw);
        // release the temporary type
        H5Tclose(type);
        // and report
        return value;
    }
    // fixed length strings come back inline; make a buffer the right size
    auto size = H5Tget_size(type);
    string_t value(size, '\0');
    // read into it
    H5Aread(id(), type, value.data());
    // release the temporary type
    H5Tclose(type);
    // trim any trailing padding and report
    value.resize(value.find('\0') == string_t::npos ? size : value.find('\0'));
    return value;
}


// write {value} into me as a string
auto
pyre::h5::Attribute::writeString(const string_t & value) const -> void
{
    // grab my datatype
    auto type = H5Aget_type(id());
    // variable length strings go out as a pointer to the contents
    if (H5Tis_variable_str(type) > 0) {
        // the library copies from the address i hand it
        const char * raw = value.data();
        H5Awrite(id(), type, &raw);
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
    H5Awrite(id(), type, buffer.data());
    // release the temporary type
    H5Tclose(type);
    // all done
    return;
}


// release my handle
auto
pyre::h5::Attribute::close() -> void
{
    // give up my reference; the library closes the attribute when the last one goes away
    _release();
    // all done
    return;
}


// end of file
