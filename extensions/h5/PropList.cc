// externals
#include "external.h"
// namespace setup
#include "forward.h"


// property lists
void
pyre::h5::py::pl(py::module & m)
{
    // add bindings for hdf5 property lists
    auto cls = py::class_<PropList>(
        // in scope
        m,
        // class name
        "PL",
        // docstring
        "a basic property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "create a property list");

    // properties
    cls.def_property_readonly(
        // the name
        "hid",
        // the implementation
        &PropList::getId,
        // the docstring
        "get my h5 handle id");

    // metamethods
    cls.def(
        // the name
        "__len__",
        // the implementation
        &PropList::getNumProps,
        // the docstring
        "the number of properties in this list");

    cls.def(
        // the name
        "__contains__",
        // the implementation
        py::overload_cast<const string_t &>(&PropList::propExist, py::const_),
        // the signature
        "name"_a,
        // the docstring
        "check whether {name} is a known property in this list");

    cls.def(
        // the name
        "__getitem__",
        // the implementation
        py::overload_cast<const string_t &>(&PropList::getProperty, py::const_),
        // the signature
        "name"_a,
        // the docstring
        "get the property associated with {name}");

    cls.def(
        // the name
        "__setitem__",
        // the implementation
        py::overload_cast<const string_t &, const string_t &>(&PropList::setProperty, py::const_),
        // the signature
        "name"_a, "value"_a,
        // the docstring
        "set the property {name} to {value}");

    cls.def(
        // the name
        "__delitem__",
        // the implementation
        py::overload_cast<const string_t &>(&PropList::removeProp, py::const_),
        // the signature
        "name"_a,
        // the docstring
        "delete the property associated with {name}");

    // interface
    // get the size of a property
    cls.def(
        // the name
        "getPropertySize",
        // the implementation
        py::overload_cast<const string_t &>(&PropList::getPropSize, py::const_),
        // the signature
        "name"_a,
        // the docstring
        "retrieve the size of the named property");

    // close the list
    cls.def(
        // the name
        "close",
        // the implementation
        &PropList::close,
        // the docstring
        "discard the property list");
}

// end of file
