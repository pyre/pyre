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
    auto getByName = [](const Group & self, const string_t & name) -> py::object {
        // get the member id
        auto hid = self.getObjId(name);
        // figure out the type of the named member
        auto type = self.childObjType(name);
        // decode the {type}
        switch (type) {
            // if it's a group
            case H5O_TYPE_GROUP:
                // dress it up and return it
                return py::cast(new Group(hid));
            // if it's a dataset
            case H5O_TYPE_DATASET:
                // dress it up and return it
                return py::cast(new DataSet(hid));
            // if it is a named type
            case H5O_TYPE_NAMED_DATATYPE:
                // dress it up and return it
                return py::cast(new DataType(hid));
            // otherwise
            default:
                break;
        }

        // bail on the other object types, for now
        return py::none();
    };

    auto getByIndex = [&getByName](const Group & self, int index) -> py::object {
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

    // the object categories
    cls.def_property_readonly_static(
        // the name
        "identifierType",
        // the implementation
        [](const py::object &) -> H5I_type_t {
            // i am a group
            return H5I_GROUP;
        },
        // the docstring
        "get my h5 identifier type");

    cls.def_property_readonly_static(
        // the name
        "objectType",
        // the implementation
        [](const py::object &) -> H5O_type_t {
            // i am a group
            return H5O_TYPE_GROUP;
        },
        // the docstring
        "get my h5 object type");

    // close the group
    cls.def(
        // the name
        "close",
        // the implementation
        &Group::close,
        // the docstring
        "close this group");

    // check whether a name corresponds to a group member
    cls.def(
        // the name
        "has",
        // the implementation
        [](const Group & self, const string_t & name) -> bool {
            // check and return the result
            return self.nameExists(name);
        },
        // the signature
        "name"_a,
        // the docstring
        "check whether {name} is a group member");

    // extract information about my members
    cls.def(
        // the name
        "members",
        // the implementation
        [](const Group & self) -> names_t {
            // make a pile
            auto members = names_t();
            // look up how many members i have and go through them
            for (auto index = 0; index < self.getNumObjs(); ++index) {
                // to get the name of the member at {index}
                auto name = self.getObjnameByIdx(index);
                // and add it to the pile
                members.emplace_back(name);
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
        "open a dataset given its {path}");

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
        "open one of my subgroups given its {path}");

    cls.def(
        // the name
        "get",
        // the implementation
        getByName,
        // the signature
        "path"_a,
        // the docstring
        "get the member at the given {path}");

    cls.def(
        // the name
        "get",
        // the implementation
        getByIndex,
        // the signature
        "index"_a,
        // the docstring
        "get the name of the member at the given {index}");

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
        "create a new group at the given {path}");

    cls.def(
        // the name
        "create",
        // the implementation
        [](const Group & self, const string_t & path, const DataType & type,
           const DataSpace & space, const DCPL & dcpl, const DAPL & dapl) -> DataSet {
            // make the dataset and return it
            return self.createDataSet(path, type, space, dcpl, dapl);
        },
        // the signature
        "path"_a, "type"_a, "space"_a, "dcpl"_a = DCPL::DEFAULT, "dapl"_a = DAPL::DEFAULT,
        // the docstring
        "create a new dataset at the given {name} given its {type} and data {space}");

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
        "__contains__",
        // the implementation
        [](const Group & self, const string_t & name) -> bool {
            // check and return the result
            return self.nameExists(name);
        },
        // the signature
        "name"_a,
        // the docstring
        "check whether {name} is a known member of this group");

    cls.def(
        // the name
        "__getitem__",
        // the implementation
        getByName,
        // the signature
        "path"_a,
        // the docstring
        "get the member at the given {path}");

    cls.def(
        // the name
        "__getitem__",
        // the implementation
        getByIndex,
        // the signature
        "index"_a,
        // the docstring
        "get the name of the member at the given {index}");

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
