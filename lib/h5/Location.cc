// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Location.h"
// the reporting of library refusals
#include "diagnostics.h"
// the types my interface mentions
#include "Attribute.h"
#include "DataSpace.h"
#include "types/Datatype.h"
#include "properties/ACPL.h"


// adopt an existing raw handle
pyre::h5::Location::Location(id_type id) : Identifier(id) {}


// the number of attributes i carry
auto
pyre::h5::Location::attributeCount() const -> int
{
    // ask the library for just the attribute count
    H5O_info2_t info;
    // an object the library will not describe carries no attributes
    if (H5Oget_info3(id(), &info, H5O_INFO_NUM_ATTRS) < 0) {
        // so say so, rather than reading an answer nobody wrote
        return 0;
    }
    // otherwise, report the count
    return static_cast<int>(info.num_attrs);
}


// the attribute at the given {index}
auto
pyre::h5::Location::openAttribute(unsigned int index) const -> Attribute
{
    // open the attribute by its position; the library hands back a fresh handle the wrapper
    // adopts, or an invalid one when there is no such attribute, which is the caller's answer
    return Attribute(
        static_cast<id_type>(H5Aopen_by_idx(
            id(), ".", H5_INDEX_NAME, H5_ITER_INC, index, H5P_DEFAULT, H5P_DEFAULT)));
}


// the attribute by the given {name}
auto
pyre::h5::Location::openAttribute(const string_t & name) const -> Attribute
{
    // open the attribute by name; the library hands back a fresh handle the wrapper adopts, or
    // an invalid one when there is no such attribute, which is the caller's answer
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
    const properties::ACPL & acpl) const -> Attribute
{
    // make the attribute; the library hands back a fresh handle the wrapper adopts
    auto hid = H5Acreate2(id(), name.data(), type.id(), space.id(), acpl.id(), H5P_DEFAULT);
    // if the library refused
    if (hid < 0) {
        // complain
        complain("pyre.h5.location", "creating the attribute '" + name + "'");
    }
    // hand off the attribute, empty if the library refused
    return Attribute(static_cast<id_type>(hid));
}


// rename the {oldName} attribute to {newName}
auto
pyre::h5::Location::renameAttribute(const string_t & oldName, const string_t & newName) const
    -> void
{
    // hand it to the library
    if (H5Arename(id(), oldName.data(), newName.data()) < 0) {
        // and complain if it refused
        complain(
            "pyre.h5.location", "renaming the attribute '" + oldName + "' to '" + newName + "'");
    }
    // all done
    return;
}


// remove the attribute by the given {name}
auto
pyre::h5::Location::removeAttribute(const string_t & name) const -> void
{
    // hand it to the library
    if (H5Adelete(id(), name.data()) < 0) {
        // and complain if it refused
        complain("pyre.h5.location", "removing the attribute '" + name + "'");
    }
    // all done
    return;
}


// end of file
