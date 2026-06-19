// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "PropList.h"


// the default property list, a handle to the library-wide defaults
pyre::h5::PropList::PropList() : Identifier(H5P_DEFAULT) {}


// adopt an existing raw handle
pyre::h5::PropList::PropList(id_type id) : Identifier(id) {}


// the number of properties in the list
auto
pyre::h5::PropList::numProps() const -> std::size_t
{
    // make room for the answer
    std::size_t count = 0;
    // ask the library
    H5Pget_nprops(id(), &count);
    // and report
    return count;
}


// whether the list has a property by the given {name}
auto
pyre::h5::PropList::exists(const string_t & name) const -> bool
{
    // ask the library; a positive answer means it is present
    return H5Pexist(id(), name.data()) > 0;
}


// the size, in bytes, of the property by the given {name}
auto
pyre::h5::PropList::propertySize(const string_t & name) const -> std::size_t
{
    // make room for the answer
    std::size_t size = 0;
    // ask the library
    H5Pget_size(id(), name.data(), &size);
    // and report
    return size;
}


// the value of the property by the given {name}, as raw bytes in a string
auto
pyre::h5::PropList::property(const string_t & name) const -> string_t
{
    // find out how big the value is
    auto size = propertySize(name);
    // make a buffer to hold it
    string_t value(size, '\0');
    // pull the raw bytes
    H5Pget(id(), name.data(), value.data());
    // and report
    return value;
}


// set the property by the given {name} to {value}
auto
pyre::h5::PropList::setProperty(const string_t & name, const string_t & value) -> void
{
    // hand the raw bytes to the library
    H5Pset(id(), name.data(), value.data());
    // all done
    return;
}


// remove the property by the given {name}
auto
pyre::h5::PropList::removeProperty(const string_t & name) -> void
{
    // ask the library to drop it
    H5Premove(id(), name.data());
    // all done
    return;
}


// release my handle
auto
pyre::h5::PropList::close() -> void
{
    // give up my reference; the library closes the list when the last one goes away
    _release();
    // all done
    return;
}


// end of file
