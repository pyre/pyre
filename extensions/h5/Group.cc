// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// objects
void
pyre::h5::py::group(py::module & m)
{
    // helpers
    auto getByName = [](const Group & self, const string_t & name) {
        // figure out the type of the named member
        auto type = self.childObjType(name);
        // if it's a group
        if (type == H5O_TYPE_GROUP) {
            // get the group id
            auto hid = self.getObjId(name);
            // and return a copy along with the type information
            return py::make_tuple(new Group(hid), type);
        }
        // if it's a dataset
        if (type == H5O_TYPE_DATASET) {
            // get the dataset id
            auto hid = self.getObjId(name);
            // and return a copy along with the type information
            return py::make_tuple(new DataSet(hid), type);
        }
        // for anything else, just return the type info
        return py::make_tuple(nullptr, type);
    };

    auto getByIndex = [&getByName](const Group & self, int index) {
        // figure out the index of the named member
        auto name = self.getObjnameByIdx(index);
        // and look it up
        return getByName(self, name);
    };

    // add bindings for hdf5 groups
    auto cls = py::class_<Group>(
        // in scope
        m,
        // class name
        "Group",
        // docstring
        "an HDF5 group");

    // properties
    cls.def_property_readonly(
        // the name
        "hid",
        // the implementation
        &Group::getId,
        // the docstring
        "get my h5 handle id");

    // close the group
    cls.def(
        // the name
        "close",
        // the implementation
        &Group::close,
        // the docstring
        "close this group");

    // extract information about my members
    cls.def(
        // the name
        "members",
        // the implementation
        [](const Group & self) {
            // we build (name, type) pairs
            using info_t = std::tuple<string_t, H5O_type_t>;
            // in a container
            using members_t = std::vector<info_t>;
            // make one
            auto members = members_t();
            // go through them
            for (auto index = 0; index < self.getNumObjs(); ++index) {
                // get the name of the member at {index}y3j
                auto name = self.getObjnameByIdx(index);
                // figure out its type
                auto type = self.childObjType(name);
                // and add the pair to the pile
                members.emplace_back(name, type);
            }
            // all done
            return members;
        },
        // the docstring
        "extract information about my members");

    // open a dataset
    cls.def(
        // the name
        "dataset",
        // the implementation
        [](const Group & self, string_t path) -> DataSet {
            // open the dataset and return it
            return self.openDataSet(path);
        },
        // the signature
        "path"_a,
        // the docstring
        "open a dataset given its path");

    // open one of my subgroups
    cls.def(
        // the name
        "group",
        // the implementation
        [](const Group & self, string_t path) -> Group {
            // open the group and return it
            return self.openGroup(path);
        },
        // the signature
        "path"_a,
        // the docstring
        "open one of my subgroups given its path");

    cls.def(
        // the name
        "get",
        // the implementation
        getByName,
        // the signature
        "path"_a,
        // the docstring
        "get the member at the given location");

    cls.def(
        // the name
        "get",
        // the implementation
        getByIndex,
        // the signature
        "index"_a,
        // the docstring
        "get the name of the member at the given index");

    // member creation
    cls.def(
        // the name
        "create",
        // the implementation
        [](const Group & self, const string_t & path) -> Group {
            // make the group and return it
            return self.createGroup(path);
        },
        // the signature
        "path"_a,
        // the docstring
        "create a new group of the given {name}");

    cls.def(
        // the name
        "create",
        // the implementation
        [](const Group & self, const string_t & path, const DataType & type,
           const DataSpace & space) -> DataSet {
            // make the dataset and return it
            return self.createDataSet(path, type, space);
        },
        // the signature
        "path"_a, "type"_a, "space"_a,
        // the docstring
        "create a new group of the given {name}");

    // metamethods
    cls.def(
        // the name
        "__len__",
        // the implementation
        [](const Group & self) {
            // all done
            return self.getNumObjs();
        },
        // the docstring
        "the number of group members");

    cls.def(
        // the name
        "__getitem__",
        // the implementation
        getByName,
        // the signature
        "path"_a,
        // the docstring
        "get the member at the given location");

    cls.def(
        // the name
        "__getitem__",
        // the implementation
        getByIndex,
        // the signature
        "index"_a,
        // the docstring
        "get the name of the member at the given location");

    cls.def(
        // the name
        "__iter__",
        // the implementation
        [](const Group & self) {
            // make an iterator and return it
            // return py::make_iterator(self.cbegin(), self.cend());
            // all done
            return;
        },
        // the docstring
        "iterate over my members",
        // keep the group around while its iterator is in use
        py::keep_alive<0, 1>());

    // all done
    return;
}


// end of file
