// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "List.h"
// the reporting of library refusals
#include "../diagnostics.h"


// the default property list, a handle to the library-wide defaults
pyre::h5::properties::List::List() : Identifier(H5P_DEFAULT) {}


// adopt an existing raw handle
pyre::h5::properties::List::List(id_type id) : Identifier(id) {}


// the number of properties in the list
auto
pyre::h5::properties::List::propertyCount() const -> std::size_t
{
    // make room for the answer
    std::size_t count = 0;
    // ask the library
    if (H5Pget_nprops(id(), &count) < 0) {
        // complain if it refused
        complain("pyre.h5.properties", "counting the properties of a list");
        // and report nothing
        return 0;
    }
    // otherwise, report
    return count;
}


// whether the list has a property by the given {name}
auto
pyre::h5::properties::List::exists(const string_t & name) const -> bool
{
    // ask the library; a positive answer means it is present
    return H5Pexist(id(), name.data()) > 0;
}


// the size, in bytes, of the property by the given {name}
auto
pyre::h5::properties::List::propertySize(const string_t & name) const -> std::size_t
{
    // make room for the answer
    std::size_t size = 0;
    // ask the library
    if (H5Pget_size(id(), name.data(), &size) < 0) {
        // complain if it refused
        complain("pyre.h5.properties", "retrieving the size of the property '" + name + "'");
        // and report nothing
        return 0;
    }
    // otherwise, report
    return size;
}


// the value of the property by the given {name}, as raw bytes in a string
auto
pyre::h5::properties::List::property(const string_t & name) const -> string_t
{
    // find out how big the value is
    auto size = propertySize(name);
    // make a buffer to hold it
    string_t value(size, '\0');
    // pull the raw bytes
    if (H5Pget(id(), name.data(), value.data()) < 0) {
        // complain if the library refused
        complain("pyre.h5.properties", "retrieving the property '" + name + "'");
        // and report nothing
        return "";
    }
    // otherwise, report
    return value;
}


// set the property by the given {name} to {value}
auto
pyre::h5::properties::List::property(const string_t & name, const string_t & value) -> void
{
    // hand the raw bytes to the library
    if (H5Pset(id(), name.data(), value.data()) < 0) {
        // and complain if it refused
        complain("pyre.h5.properties", "setting the property '" + name + "'");
    }
    // all done
    return;
}


// remove the property by the given {name}
auto
pyre::h5::properties::List::removeProperty(const string_t & name) -> void
{
    // ask the library to drop it
    if (H5Premove(id(), name.data()) < 0) {
        // and complain if it refused
        complain("pyre.h5.properties", "removing the property '" + name + "'");
    }
    // all done
    return;
}


// release my handle
auto
pyre::h5::properties::List::close() -> void
{
    // give up my reference; the library closes the list when the last one goes away
    _release();
    // all done
    return;
}


// end of file
