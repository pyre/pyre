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


// an hdf5 group: a container of named datasets, subgroups, and named datatypes
class pyre::h5::Group : public pyre::h5::Location {
    // types
public:
    // the kind of an object: group, dataset, or named datatype
    using object_type = H5O_type_t;

    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit Group(id_type id);
    // the full set of special members
    Group(const Group &) = default;
    Group(Group &&) noexcept = default;
    Group & operator=(const Group &) = default;
    Group & operator=(Group &&) noexcept = default;
    ~Group() override = default;

    // interface
public:
    // the number of members i hold
    auto memberCount() const -> hsize_t;
    // the name of the member at the given {index}
    auto memberName(unsigned int index) const -> string_t;
    // whether i hold a member by the given {name}
    auto exists(const string_t & name) const -> bool;
    // the kind of the member by the given {name}
    auto childType(const string_t & name) const -> object_type;
    // open the member by the given {name}, returning its raw handle for the caller to dress up
    auto objectId(const string_t & name) const -> id_type;

    // open the subgroup at the given {path}
    auto openGroup(const string_t & path) const -> Group;
    // open the dataset at the given {path}
    auto openDataSet(const string_t & path) const -> DataSet;
    // create a subgroup at the given {path}
    auto createGroup(const string_t & path) const -> Group;
    // create a dataset {path} of {type} over {space}, with property lists {dcpl} and {dapl}
    auto createDataSet(
        const string_t & path, const types::Datatype & type, const DataSpace & space,
        const properties::DCPL & dcpl, const properties::DAPL & dapl) const -> DataSet;

    // release my handle
    auto close() -> void;
};


// end of file
