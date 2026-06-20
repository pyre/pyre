// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Group.h"
// the members i hand back, and the types my interface mentions
#include "DataSet.h"
#include "DataSpace.h"
#include "types/Datatype.h"
#include "properties/DCPL.h"
#include "properties/DAPL.h"


// adopt an existing raw handle
pyre::h5::Group::Group(id_type id) : Location(id) {}


// the number of members i hold
auto
pyre::h5::Group::memberCount() const -> hsize_t
{
    // make room for the metadata
    H5G_info_t info;
    // ask the library
    H5Gget_info(id(), &info);
    // and report the number of links
    return info.nlinks;
}


// the name of the member at the given {index}
auto
pyre::h5::Group::memberName(unsigned int index) const -> string_t
{
    // find out how long the name is
    auto len =
        H5Lget_name_by_idx(id(), ".", H5_INDEX_NAME, H5_ITER_INC, index, nullptr, 0, H5P_DEFAULT);
    // make room for it, plus the terminating null
    string_t buffer(len + 1, '\0');
    // retrieve it
    H5Lget_name_by_idx(
        id(), ".", H5_INDEX_NAME, H5_ITER_INC, index, buffer.data(), len + 1, H5P_DEFAULT);
    // trim the terminator and report
    buffer.resize(len);
    return buffer;
}


// whether i hold a member by the given {name}
auto
pyre::h5::Group::exists(const string_t & name) const -> bool
{
    // ask the library; a positive answer means it is present
    return H5Lexists(id(), name.data(), H5P_DEFAULT) > 0;
}


// the kind of the member by the given {name}
auto
pyre::h5::Group::childType(const string_t & name) const -> object_type
{
    // ask the library for just the basic info; the info struct and accessor were renamed in
    // hdf5 1.12, so pick the spelling that matches the library we build against
#if H5_VERSION_GE(1, 12, 0)
    H5O_info2_t info;
    H5Oget_info_by_name3(id(), name.data(), &info, H5O_INFO_BASIC, H5P_DEFAULT);
#else
    H5O_info_t info;
    H5Oget_info_by_name2(id(), name.data(), &info, H5O_INFO_BASIC, H5P_DEFAULT);
#endif
    // and report the object kind
    return info.type;
}


// open the member by the given {name}, returning its raw handle for the caller to dress up
auto
pyre::h5::Group::objectId(const string_t & name) const -> id_type
{
    // open it; the library hands back a fresh handle the caller takes ownership of
    return static_cast<id_type>(H5Oopen(id(), name.data(), H5P_DEFAULT));
}


// open the subgroup at the given {path}
auto
pyre::h5::Group::openGroup(const string_t & path) const -> Group
{
    // open it; the library hands back a fresh handle the wrapper adopts
    return Group(static_cast<id_type>(H5Gopen2(id(), path.data(), H5P_DEFAULT)));
}


// open the dataset at the given {path}
auto
pyre::h5::Group::openDataSet(const string_t & path) const -> DataSet
{
    // open it; the library hands back a fresh handle the wrapper adopts
    return DataSet(static_cast<id_type>(H5Dopen2(id(), path.data(), H5P_DEFAULT)));
}


// create a subgroup at the given {path}
auto
pyre::h5::Group::createGroup(const string_t & path) const -> Group
{
    // make it with default link, creation, and access property lists; adopt the fresh handle
    return Group(
        static_cast<id_type>(H5Gcreate2(id(), path.data(), H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT)));
}


// create a dataset {path} of {type} over {space}, with property lists {dcpl} and {dapl}
auto
pyre::h5::Group::createDataSet(
    const string_t & path, const types::Datatype & type, const DataSpace & space,
    const properties::DCPL & dcpl, const properties::DAPL & dapl) const -> DataSet
{
    // make it with a default link creation property list; adopt the fresh handle
    return DataSet(
        static_cast<id_type>(H5Dcreate2(
            id(), path.data(), type.id(), space.id(), H5P_DEFAULT, dcpl.id(), dapl.id())));
}


// release my handle
auto
pyre::h5::Group::close() -> void
{
    // give up my reference; the library closes the group when the last one goes away
    _release();
    // all done
    return;
}


// end of file
