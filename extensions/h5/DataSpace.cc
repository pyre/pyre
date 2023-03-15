// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


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
        py::init<H5S_class_t>(),
        // the signature
        "type"_a = H5S_SCALAR,
        // the something
        "make a dataspace of the given type");

    // simple, with the given shape
    cls.def(
        // the implementation
        py::init([](const shape_t & shape) {
            // instantiate and return
            return new DataSpace(shape.size(), &shape[0], nullptr);
        }),
        // the signature
        "shape"_a,
        // the something
        "make a dataspace of the given shape");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "all",
        // the implementation
        [](const py::object &) {
            // easy enough
            return &DataSpace::ALL;
        },
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
        &DataSpace::getId,
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
        &DataSpace::isSimple,
        // the docstring
        "check whether i'm simple");

    // the dataspace rank
    cls.def_property_readonly(
        // the name
        "rank",
        // the implementation
        &DataSpace::getSimpleExtentNdims,
        // the docstring
        "get my rank");

    // the dataspace shape
    cls.def_property(
        // the name
        "shape",
        // the reader
        [](const DataSpace & self) -> shape_t {
            // get my rank
            auto rank = self.getSimpleExtentNdims();
            // make a correctly sized vector to hold the result
            shape_t shape(rank);
            // populate it
            self.getSimpleExtentDims(&shape[0], nullptr);
            // and return it
            return shape;
        },
        // the writer
        [](DataSpace & self, const shape_t & shape) -> void {
            // resize me
            self.setExtentSimple(shape.size(), &shape[0], nullptr);
            // all done
            return;
        },
        // the docstring
        "get and set my shape");

    // the number of cells in this dataspace
    cls.def_property_readonly(
        // the name
        "cells",
        // the implementation
        &DataSpace::getSimpleExtentNpoints,
        // the docstring
        "the number of cells of the dataspace");

    // the dataspace type
    cls.def_property_readonly(
        // the name
        "type",
        // the implementation
        &DataSpace::getSimpleExtentType,
        // the docstring
        "the type of the dataspace");

    // check the current selection
    cls.def_property_readonly(
        // the name
        "validSelection",
        // the implementation
        &DataSpace::selectValid,
        // the docstring
        "verify the current selection");

    // the bounding box of the current selection
    cls.def_property_readonly(
        // the name
        "selectionBounds",
        // the implementation
        [](const DataSpace & self) {
            // find my rank
            auto rank = self.getSimpleExtentNdims();
            // the beginning
            shape_t begin(rank);
            // and the end
            shape_t end(rank);
            // hand them both to the bbox calculator
            self.getSelectBounds(&begin[0], &end[0]);
            // and return them to the caller
            return py::make_tuple(begin, end);
        },
        // the docstring
        "get the bounding box of the current selection");

    // the number of cells in the current selection
    cls.def_property_readonly(
        // the name
        "selectedCells",
        // the implementation
        &DataSpace::getSelectNpoints,
        // the docstring
        "get the number of cells in the current selection");

    // the number of elements in the current selection
    cls.def_property_readonly(
        // the name
        "selectedElements",
        // the implementation
        &DataSpace::getSelectElemNpoints,
        // the docstring
        "get the number of elements in the current selection");

    // the number of hyperslabs in the current selection
    cls.def_property_readonly(
        // the name
        "selectedSlabs",
        // the implementation
        &DataSpace::getSelectHyperNblocks,
        // the docstring
        "get the number of hyperslabs in the current selection");

    // interface
    // clear the dataspace
    cls.def(
        // the name
        "clear",
        // the implementation
        &DataSpace::setExtentNone,
        // the docstring
        "clear the dataspace, i.e. empty its extent");

    // clone the dataspace
    cls.def(
        // the name
        "clone",
        // the implementation
        [](const DataSpace & self) {
            // make a new dataspace of the same type
            auto clone = new DataSpace(self.getSimpleExtentType());
            // use me as a template
            clone->copy(self);
            // wrap in a handler and return it
            return std::unique_ptr<DataSpace>(clone);
        },
        // the docstring
        "clear the dataspace, i.e. empty its extent");

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
        [](DataSpace & self, const shape_t & shape) -> void {
            // resize me
            self.setExtentSimple(shape.size(), &shape[0], nullptr);
            // all done
            return;
        },
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
        [](const DataSpace & self, const offsets_t & delta) -> void {
            // apply the offset
            self.offsetSimple(&delta[0]);
            // all done
            return;
        },
        // the signature
        "delta"_a,
        // the docstring
        "offset the current selection by the given {delta}");

    // element selection
    cls.def(
        // the name
        "selectElements",
        // the implementation
        [](DataSpace & self, H5S_seloper_t op, points_t elements) {
            // make a pile
            auto pile = new hsize_t[elements.size() * elements[0].size()];
            // starting at 0
            auto cursor = 0;
            // go through the points
            for (const auto & element : elements) {
                // and their coordinates
                for (const auto & index : element) {
                    // transfer the {index} to the {pile}
                    pile[cursor++] = index;
                }
            }
            // combine the {elements} with the current selection
            self.selectElements(op, elements.size(), pile);
            // clean up
            delete[] pile;
            // all done
            return;
        },
        // the signature
        "op"_a, "elements"_a,
        // the docstring
        "combine the given {elements} with the current selection");

    // grab (a portion of) the list of elements in the current selection
    cls.def(
        // the name
        "getSelectedElements",
        // the implementation
        [](const DataSpace & self, int start) {
            // get my rank
            auto rank = self.getSimpleExtentNdims();
            // get the number of selected elements
            auto len = self.getSelectElemNpoints();
            // make a pile
            auto pile = new hsize_t[len * rank];
            // populate it
            self.getSelectElemPointlist(0, len, pile);
            // build the coordinate table
            points_t points;
            // go through the points
            for (auto p = start; p < len; ++p) {
                // build a vector to hold the coordinates and add it to the pile
                auto & point = points.emplace_back(rank);
                // populate the coordinates
                for (auto index = 0; index < rank; ++index) {
                    // by copying each index to the right spot
                    point[index] = pile[p * rank + index];
                }
            }
            // clean up
            delete[] pile;
            // and return the points
            return points;
        },
        // the signature
        "start"_a = 0,
        // the docstring
        "get the list of elements in the current selection");

    // slab selection
    cls.def(
        // the name
        "slab",
        // the implementation
        [](const DataSpace & self, const index_t & origin, const shape_t & shape) {
            // the block count
            shape_t count;
            // we only want one block
            count.assign(shape.size(), 1);
            // set the selection to the given slab
            self.selectHyperslab(H5S_SELECT_SET, &count[0], &origin[0], nullptr, &shape[0]);
            // all done
            return;
        },
        // the signature
        "origin"_a, "shape"_a,
        // the docstring
        "select a slab of the given {shape} at the given {origin}");

    cls.def(
        // the name
        "slab",
        // the implementation
        [](const DataSpace & self, H5S_seloper_t op, const index_t & origin,
           const shape_t & shape) {
            // the block count
            shape_t count;
            // we only want one block
            count.assign(shape.size(), 1);
            // set the selection to the given slab
            self.selectHyperslab(op, &count[0], &origin[0], nullptr, &shape[0]);
            // all done
            return;
        },
        // the signature
        "op"_a, "origin"_a, "shape"_a,
        // the docstring
        "use {op} to combine the specified slab with the current selection");

    cls.def(
        // the name
        "slab",
        // the implementation
        [](const DataSpace & self, H5S_seloper_t op, const shape_t & origin, const shape_t & shape,
           const shape_t & stride, const shape_t & count) {
            // select the slab
            self.selectHyperslab(op, &count[0], &origin[0], &stride[0], &shape[0]);
            // all done
            return;
        },
        // the signature
        "op"_a, "origin"_a, "shape"_a, "stride"_a, "count"_a,
        // the docstring
        "combine a fully specified hyperslab with the current selection");

    // grab (a portion of) the list of selected slabs
    cls.def(
        // the name
        "getSelectedSlabs",
        // the implementation
        [](const DataSpace & self, int start) {
            // get my rank
            auto rank = self.getSimpleExtentNdims();
            // get the selection size
            auto len = self.getSelectHyperNblocks();
            // compute the number of blocks we will extract
            auto blocks = len - start;
            // make a pile for the slabs, formatted as a (begin,end) pair for each slab
            auto pile = new hsize_t[2 * rank * blocks];
            // populate it
            self.getSelectHyperBlocklist(start, blocks, pile);
            // build the result
            std::vector<std::pair<shape_t, shape_t>> slabs;
            // go through them
            for (auto block = 0; block < blocks; ++block) {
                // compute the location of this block
                auto cursor = pile + 2 * rank * (block + start);
                // set up the beginning of the block
                shape_t begin(rank);
                // populate it
                std::copy(cursor, cursor + rank, begin.begin());
                // set up the end of the block
                shape_t end(rank);
                // skip to the beginning of the end block
                cursor += rank;
                // and populate it
                std::copy(cursor, cursor + rank, end.begin());
                // add the pair to the pile
                slabs.emplace_back(begin, end);
            }
            // clean up
            delete[] pile;
            // return the harvested slabs
            return slabs;
        },
        // the signature
        "start"_a = 0,
        // the docstring
        "get the list of selected hyperslabs");

    // all done
    return;
}


// end of file
