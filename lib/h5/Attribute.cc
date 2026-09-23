// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Attribute.h"
// the reporting of library refusals
#include "diagnostics.h"
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
    // if the library would not say
    if (len < 0) {
        // complain
        complain("pyre.h5.attribute", "retrieving the name of an attribute");
        // and there is no name
        return "";
    }
    // make room for it, plus the terminating null the library writes
    string_t buffer(len + 1, '\0');
    // retrieve it; the library will not change its mind between the two calls
    if (H5Aget_name(id(), len + 1, buffer.data()) < 0) {
        // unless something is badly wrong
        complain("pyre.h5.attribute", "retrieving the name of an attribute");
        // in which case there is no name
        return "";
    }
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
    // if the library would not hand it over
    if (type < 0) {
        // complain
        complain("pyre.h5.attribute", "retrieving the datatype of an attribute");
        // and there is no class to report
        return H5T_NO_CLASS;
    }
    // read its class; the library answers with {H5T_NO_CLASS} when it cannot tell
    auto cls = H5Tget_class(type);
    // if it could not
    if (cls == H5T_NO_CLASS) {
        // complain
        complain("pyre.h5.attribute", "retrieving the datatype class of an attribute");
    }
    // give the temporary type back
    if (H5Tclose(type) < 0) {
        // and complain if the library would not take it
        complain("pyre.h5.attribute", "releasing the datatype of an attribute");
    }
    // and report
    return cls;
}


// my datatype, as a fresh owned wrapper
auto
pyre::h5::Attribute::datatype() const -> types::Datatype
{
    // {H5Aget_type} hands back a fresh handle the wrapper adopts
    auto hid = H5Aget_type(id());
    // if the library refused
    if (hid < 0) {
        // complain
        complain("pyre.h5.attribute", "retrieving the datatype of an attribute");
    }
    // hand off the type, empty if the library refused
    return types::Datatype(static_cast<id_type>(hid));
}


// my dataspace, as a fresh owned wrapper
auto
pyre::h5::Attribute::dataspace() const -> DataSpace
{
    // {H5Aget_space} hands back a fresh handle the wrapper adopts
    auto hid = H5Aget_space(id());
    // if the library refused
    if (hid < 0) {
        // complain
        complain("pyre.h5.attribute", "retrieving the dataspace of an attribute");
    }
    // hand off the space, empty if the library refused
    return DataSpace(static_cast<id_type>(hid));
}


// my on-disk size, in bytes
auto
pyre::h5::Attribute::storageSize() const -> hsize_t
{
    // ask the library; it answers with zero when it cannot tell, and an attribute it will not
    // describe takes up no room, so the answer is the caller's
    return H5Aget_storage_size(id());
}


// my in-memory size, in bytes
auto
pyre::h5::Attribute::memorySize() const -> std::size_t
{
    // my number of elements comes from my dataspace
    auto space = H5Aget_space(id());
    // if the library would not hand it over
    if (space < 0) {
        // complain
        complain("pyre.h5.attribute", "retrieving the dataspace of an attribute");
        // and there is no size to report
        return 0;
    }
    // count the cells
    auto points = H5Sget_simple_extent_npoints(space);
    // give the temporary space back
    if (H5Sclose(space) < 0) {
        // and complain if the library would not take it
        complain("pyre.h5.attribute", "releasing the dataspace of an attribute");
    }
    // if the library would not count
    if (points < 0) {
        // complain
        complain("pyre.h5.attribute", "counting the cells of an attribute");
        // and there is no size to report
        return 0;
    }
    // the size of each comes from my datatype
    auto type = H5Aget_type(id());
    // if the library would not hand it over
    if (type < 0) {
        // complain
        complain("pyre.h5.attribute", "retrieving the datatype of an attribute");
        // and there is no size to report
        return 0;
    }
    // measure the cell; the library answers with zero when it cannot tell
    auto size = H5Tget_size(type);
    // give the temporary type back
    if (H5Tclose(type) < 0) {
        // and complain if the library would not take it
        complain("pyre.h5.attribute", "releasing the datatype of an attribute");
    }
    // if the library would not measure
    if (size == 0) {
        // complain
        complain("pyre.h5.attribute", "measuring the cells of an attribute");
        // and there is no size to report
        return 0;
    }
    // the total is the product
    return static_cast<std::size_t>(points) * size;
}


// read my raw value, interpreted as {memtype}, into {buffer}
auto
pyre::h5::Attribute::read(id_type memtype, void * buffer) const -> void
{
    // hand it to the library
    if (H5Aread(id(), memtype, buffer) < 0) {
        // and complain if it refused
        complain("pyre.h5.attribute", "reading an attribute");
    }
    // all done
    return;
}


// write {buffer}, interpreted as {memtype}, into me
auto
pyre::h5::Attribute::write(id_type memtype, const void * buffer) const -> void
{
    // hand it to the library
    if (H5Awrite(id(), memtype, buffer) < 0) {
        // and complain if it refused
        complain("pyre.h5.attribute", "writing an attribute");
    }
    // all done
    return;
}


// read my value as a string
auto
pyre::h5::Attribute::readString() const -> string_t
{
    // grab my datatype
    auto type = H5Aget_type(id());
    // if the library would not hand it over
    if (type < 0) {
        // complain
        complain("pyre.h5.attribute", "retrieving the datatype of an attribute");
        // and there is nothing to read
        return "";
    }
    // find out whether the string is of variable length
    auto variable = H5Tis_variable_str(type);
    // if the library would not say
    if (variable < 0) {
        // complain
        complain("pyre.h5.attribute", "retrieving the string layout of an attribute");
        // release the temporary type
        if (H5Tclose(type) < 0) {
            // complaining if the library would not take it
            complain("pyre.h5.attribute", "releasing the datatype of an attribute");
        }
        // and there is nothing to read
        return "";
    }
    // variable length strings come back as a library-allocated pointer
    if (variable > 0) {
        // make room for the pointer
        char * raw = nullptr;
        // read it
        if (H5Aread(id(), type, &raw) < 0) {
            // complaining if the library refused
            complain("pyre.h5.attribute", "reading an attribute");
        }
        // copy it into a managed string; a refused read left the pointer empty
        string_t value(raw ? raw : "");
        // give the library's buffer back, if there is one
        if (raw && H5free_memory(raw) < 0) {
            // complaining if the library would not take it
            complain("pyre.h5.attribute", "releasing the buffer of an attribute");
        }
        // release the temporary type
        if (H5Tclose(type) < 0) {
            // complaining if the library would not take it
            complain("pyre.h5.attribute", "releasing the datatype of an attribute");
        }
        // and report
        return value;
    }
    // fixed length strings come back inline; measure them
    auto size = H5Tget_size(type);
    // if the library would not measure
    if (size == 0) {
        // complain
        complain("pyre.h5.attribute", "measuring the string of an attribute");
        // release the temporary type
        if (H5Tclose(type) < 0) {
            // complaining if the library would not take it
            complain("pyre.h5.attribute", "releasing the datatype of an attribute");
        }
        // and there is nothing to read
        return "";
    }
    // make a buffer the right size
    string_t value(size, '\0');
    // read into it
    if (H5Aread(id(), type, value.data()) < 0) {
        // complaining if the library refused
        complain("pyre.h5.attribute", "reading an attribute");
        // in which case the buffer holds nothing
        value.clear();
    }
    // release the temporary type
    if (H5Tclose(type) < 0) {
        // complaining if the library would not take it
        complain("pyre.h5.attribute", "releasing the datatype of an attribute");
    }
    // trim any trailing padding and report
    value.resize(value.find('\0') == string_t::npos ? value.size() : value.find('\0'));
    return value;
}


// write {value} into me as a string
auto
pyre::h5::Attribute::writeString(const string_t & value) const -> void
{
    // grab my datatype
    auto type = H5Aget_type(id());
    // if the library would not hand it over
    if (type < 0) {
        // complain
        complain("pyre.h5.attribute", "retrieving the datatype of an attribute");
        // and there is nowhere to write
        return;
    }
    // find out whether the string is of variable length
    auto variable = H5Tis_variable_str(type);
    // if the library would not say
    if (variable < 0) {
        // complain
        complain("pyre.h5.attribute", "retrieving the string layout of an attribute");
        // release the temporary type
        if (H5Tclose(type) < 0) {
            // complaining if the library would not take it
            complain("pyre.h5.attribute", "releasing the datatype of an attribute");
        }
        // and there is nowhere to write
        return;
    }
    // variable length strings go out as a pointer to the contents
    if (variable > 0) {
        // the library copies from the address i hand it
        const char * raw = value.data();
        // write it
        if (H5Awrite(id(), type, &raw) < 0) {
            // complaining if the library refused
            complain("pyre.h5.attribute", "writing an attribute");
        }
        // release the temporary type
        if (H5Tclose(type) < 0) {
            // complaining if the library would not take it
            complain("pyre.h5.attribute", "releasing the datatype of an attribute");
        }
        // all done
        return;
    }
    // fixed length strings go out inline; measure the stored size
    auto size = H5Tget_size(type);
    // if the library would not measure
    if (size == 0) {
        // complain
        complain("pyre.h5.attribute", "measuring the string of an attribute");
        // release the temporary type
        if (H5Tclose(type) < 0) {
            // complaining if the library would not take it
            complain("pyre.h5.attribute", "releasing the datatype of an attribute");
        }
        // and there is nowhere to write
        return;
    }
    // pad the value out to the stored size
    string_t buffer = value;
    buffer.resize(size, '\0');
    // write it
    if (H5Awrite(id(), type, buffer.data()) < 0) {
        // complaining if the library refused
        complain("pyre.h5.attribute", "writing an attribute");
    }
    // release the temporary type
    if (H5Tclose(type) < 0) {
        // complaining if the library would not take it
        complain("pyre.h5.attribute", "releasing the datatype of an attribute");
    }
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
