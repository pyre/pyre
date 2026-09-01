// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// code guard
#pragma once

// externals
#include "external.h"
// forward declarations
#include "forward.h"
// the datatype i deduce, the dataspaces i build, and the dataset i drive
#include "types/Datatype.h"
#include "DataSpace.h"
#include "DataSet.h"


// read from a {dataset} into a {pyre::grid} assuming that the description of the memory
// layout can be deduced automatically
template <class gridT>
auto
pyre::h5::read(
    // the dataset we are reading from
    const dataset_t & dataset,
    // the location to start reading from
    const typename gridT::index_type & origin,
    // the shape of the block
    const typename gridT::shape_type & shape,
    // and the strides, which lets us implement zoom directly
    const typename gridT::index_type & stride) -> gridT
{
    // deduce the memory layout description
    const datatype_t & memtype = datatype<typename gridT::value_type>();
    // and delegate
    return read(dataset, memtype, origin, shape, stride);
}


// read from a {dataset} into a {pyre::grid} assuming that the caller can supply
// a correct description for the memory layout
template <class gridT>
auto
pyre::h5::read(
    // the dataset we are reading from
    const dataset_t & dataset,
    // the memory layout description
    const datatype_t & datatype,
    // the location to start reading from
    const typename gridT::index_type & origin,
    // and the shape of the block
    const typename gridT::shape_type & shape,
    // and the strides, which lets us implement zoom directly
    const typename gridT::index_type & stride) -> gridT
{
    // alias my grid type and its parts
    using grid_t = gridT;
    using packing_t = typename gridT::packing_type;
    using storage_t = typename gridT::storage_type;
    // the rank of the request
    constexpr auto rank = gridT::shape_type::rank();

    // we need to express {origin}, {shape}, and {stride} as {hsize_t} coordinates
    auto cast = [](auto i) -> hsize_t {
        return static_cast<hsize_t>(i);
    };
    // the start of the target region, its extent, and its stride, which gives us zoom
    shape_t loc(rank), count(rank), skip(rank);
    std::transform(origin.begin(), origin.end(), loc.begin(), cast);
    std::transform(shape.begin(), shape.end(), count.begin(), cast);
    std::transform(stride.begin(), stride.end(), skip.begin(), cast);
    // each selected coordinate stands for a single element
    shape_t block(rank, 1);

    // ask the dataset for its dataspace and restrict it to the strided target region
    auto fileSpace = dataset.dataspace();
    fileSpace.slab(H5S_SELECT_SET, loc, block, skip, count);
    // make an in-memory dataspace matching the tile
    auto memSpace = dataspace_t(count);
    // make my grid over a fresh block sized to hold the requested tile
    auto grid = grid_t { packing_t(shape), storage_t { shape.cells() } };

    // read the data into my {grid}; everything is a pyre wrapper, so hand over the raw ids
    dataset.read(datatype.id(), grid.data(), memSpace.id(), fileSpace.id());

    // return the populated grid
    return grid;
}

// generics
template <class memT>
auto
pyre::h5::read(
    // the dataset we are reading from
    const dataset_t & self,
    // the destination
    memT & data,
    // the destination datatype
    const datatype_t & memtype,
    // the location to read from
    const shape_t & origin,
    // the shape of the read region
    const shape_t & shape) -> void
{
    // work out how many cells the tile holds
    hsize_t cells = 1;
    for (auto extent : shape) {
        cells *= extent;
    }
    // the destination has to be able to hold them
    if (static_cast<hsize_t>(data.cells()) < cells) {
        // if it cannot, make a channel
        auto channel = pyre::journal::error_t("pyre.h5");
        // complain
        channel
            // what
            << "the destination is too small for the tile"
            << pyre::journal::newline
            // details
            << "it holds " << data.cells() << " cells, and the tile has "
            << cells
            // where
            << pyre::journal::endl(__HERE__);
        // and bail, rather than let the library write past the end of the buffer
        return;
    }
    // describe the destination with the SHAPE of the tile, rather than as a flat run of the
    // same number of cells. the two hold the same elements and the library accepts either,
    // so this looks like a matter of taste -- it is not. a destination whose rank does not
    // match the source's cannot be filled by the path that hands over a whole chunk, so the
    // library falls back to a general scatter and inflates the chunk again on every read,
    // however much of it is already sitting in the chunk cache
    auto memspace = dataspace_t(shape);
    // restrict the dataset's dataspace to the region of interest
    auto filespace = self.dataspace();
    filespace.slab(origin, shape);
    // populate the buffer; {memtype} is a pyre wrapper, so hand over its raw type and space ids
    self.read(memtype.id(), data.data(), memspace.id(), filespace.id());
    // all done
    return;
}

// the same, visiting only every {stride}-th cell along each axis
template <class memT>
auto
pyre::h5::read(
    // the dataset we are reading from
    const dataset_t & self,
    // the destination
    memT & data,
    // the destination datatype
    const datatype_t & memtype,
    // the location to read from
    const shape_t & origin,
    // the number of samples to bring back along each axis
    const shape_t & shape,
    // and how far apart in the file consecutive samples sit
    const shape_t & stride) -> void
{
    // work out how many cells come back
    hsize_t cells = 1;
    for (auto extent : shape) {
        cells *= extent;
    }
    // the destination has to be able to hold them
    if (static_cast<hsize_t>(data.cells()) < cells) {
        // if it cannot, make a channel
        auto channel = pyre::journal::error_t("pyre.h5");
        // complain
        channel
            // what
            << "the destination is too small for the tile"
            << pyre::journal::newline
            // details
            << "it holds " << data.cells() << " cells, and the tile has "
            << cells
            // where
            << pyre::journal::endl(__HERE__);
        // and bail, rather than let the library write past the end of the buffer
        return;
    }
    // the samples arrive packed, so the destination is shaped like the sample grid rather
    // than like the region they were drawn from
    auto memspace = dataspace_t(shape);
    // each selected coordinate stands for a single cell, not a run of them
    shape_t block(shape.size(), 1);
    // restrict the dataset's dataspace to the strided region: {shape} blocks of one cell,
    // spaced {stride} apart, starting at {origin}
    auto filespace = self.dataspace();
    filespace.slab(H5S_SELECT_SET, origin, block, stride, shape);
    // populate the buffer; {memtype} is a pyre wrapper, so hand over its raw type and space ids
    self.read(memtype.id(), data.data(), memspace.id(), filespace.id());
    // all done
    return;
}

template <class memT>
auto
pyre::h5::write(
    const dataset_t & self, memT & data, const datatype_t & memtype, const shape_t & origin,
    const shape_t & shape) -> void
{
    // pretend the memory buffer is the same shape as the incoming tile
    auto memspace = dataspace_t(shape);
    // restrict the dataset's dataspace to the region of interest
    auto filespace = self.dataspace();
    filespace.slab(origin, shape);
    // populate the buffer; {memtype} is a pyre wrapper, so hand over its raw type and space ids
    self.write(memtype.id(), data.data(), memspace.id(), filespace.id());
    // all done
    return;
}

// the same, laying the cells down every {stride}-th slot along each axis
template <class memT>
auto
pyre::h5::write(
    const dataset_t & self, memT & data, const datatype_t & memtype, const shape_t & origin,
    const shape_t & shape, const shape_t & stride) -> void
{
    // the cells arrive packed, so the source is shaped like the sample grid rather than like
    // the region they are about to be scattered over
    auto memspace = dataspace_t(shape);
    // each selected coordinate stands for a single cell, not a run of them
    shape_t block(shape.size(), 1);
    // restrict the dataset's dataspace to the strided region: {shape} blocks of one cell,
    // spaced {stride} apart, starting at {origin}
    auto filespace = self.dataspace();
    filespace.slab(H5S_SELECT_SET, origin, block, stride, shape);
    // drain the buffer; {memtype} is a pyre wrapper, so hand over its raw type and space ids
    self.write(memtype.id(), data.data(), memspace.id(), filespace.id());
    // all done
    return;
}

template <class gridT>
auto
pyre::h5::readGrid(
    const dataset_t & self, gridT & data, const datatype_t & memtype, const shape_t & origin,
    const shape_t & shape) -> void
{
    // get a mutable copy of my storage handle
    auto storage = data.storage();
    // access the underlying store and delegate
    read(self, storage, memtype, origin, shape);
    // all done
    return;
}


template <class gridT>
auto
pyre::h5::writeGrid(
    const dataset_t & self, gridT & data, const datatype_t & memtype, const shape_t & origin,
    const shape_t & shape) -> void
{
    // get a mutable copy of my storage handle
    auto storage = data.storage();
    // access the underlying store and delegate
    write(self, storage, memtype, origin, shape);
    // all done
    return;
}


// end of file
