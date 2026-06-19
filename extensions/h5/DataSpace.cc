// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// dataspaces
void
pyre::h5::py::dataspace(py::module & m)
{
    // add bindings for hdf5 dataspaces
    auto cls = py::class_<DataSpace>(
        // in scope
        m,
        // class name
        "DataSpace",
        // docstring
        "an HDF5 dataspace");

    // constructors
    // of a given class, "scalar" by default
    cls.def(
        // the implementation
        py::init<DataSpace::class_type>(),
        // the signature
        "type"_a = H5S_SCALAR,
        // the something
        "make a dataspace of the given type");

    // simple, with the given shape
    cls.def(
        // the implementation
        py::init<const shape_t &>(),
        // the signature
        "shape"_a,
        // the something
        "make a dataspace of the given shape");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "all",
        // the implementation
        [](const py::object &) -> const DataSpace & {
            // easy enough
            return DataSpace::all();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default dataspace object");

    cls.def_property_readonly_static(
        // the name
        "ops",
        // the implementation
        [m](const py::object &) -> py::object {
            // easy enough
            return m.attr("SelectionOperator");
        },
        // docstring
        "convenient access to the dataspace selection operator enums");

    // my h5 handle
    cls.def_property_readonly(
        // the name
        "hid",
        // the implementation
        &DataSpace::id,
        // the docstring
        "get my h5 handle id");

    // the object category
    cls.def_property_readonly_static(
        // the name
        "category",
        // the implementation
        [](const py::object &) -> H5I_type_t {
            // i am a dataspace
            return H5I_DATASPACE;
        },
        // the docstring
        "get my h5 object category");

    // flag that indicates whether this dataspace is simple
    cls.def_property_readonly(
        // the name
        "simple",
        // the implementation
        &DataSpace::simple,
        // the docstring
        "check whether i'm simple");

    // the dataspace rank
    cls.def_property_readonly(
        // the name
        "rank",
        // the implementation
        &DataSpace::rank,
        // the docstring
        "get my rank");

    // the dataspace shape
    cls.def_property(
        // the name
        "shape",
        // the reader
        &DataSpace::shape,
        // the writer
        &DataSpace::reshape,
        // the docstring
        "get and set my shape");

    // the number of cells in this dataspace
    cls.def_property_readonly(
        // the name
        "cells",
        // the implementation
        &DataSpace::cells,
        // the docstring
        "the number of cells of the dataspace");

    // the dataspace type
    cls.def_property_readonly(
        // the name
        "type",
        // the implementation
        &DataSpace::type,
        // the docstring
        "the type of the dataspace");

    // check the current selection
    cls.def_property_readonly(
        // the name
        "validSelection",
        // the implementation
        &DataSpace::validSelection,
        // the docstring
        "verify the current selection");

    // the bounding box of the current selection
    cls.def_property_readonly(
        // the name
        "selectionBounds",
        // the implementation
        &DataSpace::selectionBounds,
        // the docstring
        "get the bounding box of the current selection");

    // the number of cells in the current selection
    cls.def_property_readonly(
        // the name
        "selectedCells",
        // the implementation
        &DataSpace::selectedCells,
        // the docstring
        "get the number of cells in the current selection");

    // the number of elements in the current selection
    cls.def_property_readonly(
        // the name
        "selectedElements",
        // the implementation
        &DataSpace::selectedElements,
        // the docstring
        "get the number of elements in the current selection");

    // the number of hyperslabs in the current selection
    cls.def_property_readonly(
        // the name
        "selectedSlabs",
        // the implementation
        &DataSpace::selectedSlabs,
        // the docstring
        "get the number of hyperslabs in the current selection");

    // interface
    // clear the dataspace
    cls.def(
        // the name
        "clear",
        // the implementation
        &DataSpace::clear,
        // the docstring
        "clear the dataspace, i.e. empty its extent");

    // clone the dataspace
    cls.def(
        // the name
        "clone",
        // the implementation
        &DataSpace::clone,
        // the docstring
        "make a copy of the dataspace");

    // close the dataspace
    cls.def(
        // the name
        "close",
        // the implementation
        &DataSpace::close,
        // the docstring
        "close the dataspace");

    // resize the dataspace
    cls.def(
        // the name
        "reshape",
        // the implementation
        &DataSpace::reshape,
        // the signature
        "shape"_a,
        // the docstring
        "resize this dataspace to the new {shape}");

    // selections
    cls.def(
        // the name
        "selectAll",
        // the implementation
        &DataSpace::selectAll,
        // the docstring
        "select the entire dataspace");

    cls.def(
        // the name
        "selectNone",
        // the implementation
        &DataSpace::selectNone,
        // the docstring
        "clear the dataspace selection");

    // offset the current selection
    cls.def(
        // the name
        "offset",
        // the implementation
        &DataSpace::offset,
        // the signature
        "delta"_a,
        // the docstring
        "offset the current selection by the given {delta}");

    // element selection
    cls.def(
        // the name
        "selectElements",
        // the implementation
        &DataSpace::selectElements,
        // the signature
        "op"_a, "elements"_a,
        // the docstring
        "combine the given {elements} with the current selection");

    // grab (a portion of) the list of elements in the current selection
    cls.def(
        // the name
        "getSelectedElements",
        // the implementation
        &DataSpace::selectedElementList,
        // the signature
        "start"_a = 0,
        // the docstring
        "get the list of elements in the current selection");

    // slab selection
    cls.def(
        // the name
        "slab",
        // the implementation
        py::overload_cast<const index_t &, const shape_t &>(&DataSpace::slab),
        // the signature
        "origin"_a, "shape"_a,
        // the docstring
        "select a slab of the given {shape} at the given {origin}");

    cls.def(
        // the name
        "slab",
        // the implementation
        py::overload_cast<DataSpace::selection_type, const index_t &, const shape_t &>(
            &DataSpace::slab),
        // the signature
        "op"_a, "origin"_a, "shape"_a,
        // the docstring
        "use {op} to combine the specified slab with the current selection");

    cls.def(
        // the name
        "slab",
        // the implementation
        py::overload_cast<
            DataSpace::selection_type, const shape_t &, const shape_t &, const shape_t &,
            const shape_t &>(&DataSpace::slab),
        // the signature
        "op"_a, "origin"_a, "shape"_a, "stride"_a, "count"_a,
        // the docstring
        "combine a fully specified hyperslab with the current selection");

    // grab (a portion of) the list of selected slabs
    cls.def(
        // the name
        "getSelectedSlabs",
        // the implementation
        &DataSpace::selectedSlabList,
        // the signature
        "start"_a = 0,
        // the docstring
        "get the list of selected hyperslabs");

    // all done
    return;
}


// end of file
