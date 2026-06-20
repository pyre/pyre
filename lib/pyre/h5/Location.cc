// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Location.h"
// the types my interface mentions
#include "Attribute.h"
#include "DataSpace.h"
#include "types/Datatype.h"
#include "properties/List.h"


// adopt an existing raw handle
pyre::h5::Location::Location(id_type id) : Identifier(id) {}


// the number of attributes i carry
auto
pyre::h5::Location::attributeCount() const -> int
{
    // make room for the metadata
    H5O_info2_t info;
    // ask the library for just the attribute count
    H5Oget_info3(id(), &info, H5O_INFO_NUM_ATTRS);
    // and report it
    return static_cast<int>(info.num_attrs);
}


// the attribute at the given {index}
auto
pyre::h5::Location::openAttribute(unsigned int index) const -> Attribute
{
    // open the attribute by its position; the library hands back a fresh handle the wrapper adopts
    return Attribute(
        static_cast<id_type>(H5Aopen_by_idx(
            id(), ".", H5_INDEX_NAME, H5_ITER_INC, index, H5P_DEFAULT, H5P_DEFAULT)));
}


// the attribute by the given {name}
auto
pyre::h5::Location::openAttribute(const string_t & name) const -> Attribute
{
    // open the attribute by name; the library hands back a fresh handle the wrapper adopts
    return Attribute(static_cast<id_type>(H5Aopen(id(), name.data(), H5P_DEFAULT)));
}


// whether i carry an attribute by the given {name}
auto
pyre::h5::Location::hasAttribute(const string_t & name) const -> bool
{
    // ask the library; a positive answer means it is present
    return H5Aexists(id(), name.data()) > 0;
}


// create an attribute {name} of {type} over {space}, with creation property list {acpl}
auto
pyre::h5::Location::createAttribute(
    const string_t & name, const types::Datatype & type, const DataSpace & space,
    const properties::List & acpl) const -> Attribute
{
    // make the attribute; the library hands back a fresh handle the wrapper adopts
    return Attribute(
        static_cast<id_type>(
            H5Acreate2(id(), name.data(), type.id(), space.id(), acpl.id(), H5P_DEFAULT)));
}


// rename the {oldName} attribute to {newName}
auto
pyre::h5::Location::renameAttribute(const string_t & oldName, const string_t & newName) const
    -> void
{
    // hand it to the library
    H5Arename(id(), oldName.data(), newName.data());
    // all done
    return;
}


// remove the attribute by the given {name}
auto
pyre::h5::Location::removeAttribute(const string_t & name) const -> void
{
    // hand it to the library
    H5Adelete(id(), name.data());
    // all done
    return;
}


// end of file
