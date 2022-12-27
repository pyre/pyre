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


    // flag that indicates whether this dataspace is simple
    cls.def_property_readonly(
        // the name
        "simple",
        // the reader
        &DataSpace::isSimple,
        // the docstring
        "check whether i'm simple");


    // the dataspace shape
    cls.def_property(
        // the name
        "shape",
        // the reader
        [](const DataSpace & self) -> dims_t {
            // get my rank
            auto rank = self.getSimpleExtentNdims();
            // make a correctly sized vector to hold the result
            dims_t shape(rank);
            // populate it
            self.getSimpleExtentDims(&shape[0], nullptr);
            // and return it
            return shape;
        },
        // the writer
        [](DataSpace & self, const dims_t & shape) -> void {
            // all done
            return;
        },
        // the docstring
        "get the shape of the dataset");


    // all done
    return;
}


// end of file
