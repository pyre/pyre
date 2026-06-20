// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// code guard
#pragma once

// externals
#include "external.h"
// forward declarations
#include "forward.h"
// the datatype i deduce and the dataset i drive
#include "types/Datatype.h"
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
    using shape_t = typename gridT::shape_type;
    using packing_t = typename gridT::packing_type;
    // alias the {hdf5} dataspace types
    using h5info_t = std::array<hsize_t, shape_t::rank()>;

    // set up the file data space
    // we need something that converts into {hsize_t} from whatever types {origin},
    // {shape}, and {strides} use to represent their coordinates
    auto cast = [](auto i) -> hsize_t {
        return static_cast<hsize_t>(i);
    };
    // convert the {origin} into an array of {hsize_t}
    // make some room
    h5info_t loc;
    // populate
    std::transform(origin.begin(), origin.end(), loc.begin(), cast);
    // repeat for the {shape}
    h5info_t count;
    // populate
    std::transform(shape.begin(), shape.end(), count.begin(), cast);
    // and the strides
    h5info_t skip;
    // populate
    std::transform(stride.begin(), stride.end(), skip.begin(), cast);
    // ask the dataset for its dataspace, bridged into an {H5::} one for the selection machinery
    auto fileSpace = H5::DataSpace(dataset.dataspace().id());
    // select the hyperslab that corresponds to our target region
    fileSpace.selectHyperslab(H5S_SELECT_SET, &count[0], &loc[0], &skip[0]);

    // make a dataspace
    auto memSpace = dataspace_t(shape.rank(), &count[0]);
    // make my grid
    auto grid = grid_t { packing_t(shape), shape.cells() };

    // read the data into my {grid}; {datatype} is a pyre wrapper, so hand the dataset its raw
    // type id and the raw space ids
    dataset.read(datatype.id(), grid.data()->data(), memSpace.getId(), fileSpace.getId());

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
    // get the size of the buffer
    hsize_t memsize = data.cells();
    // the in-memory layout is one-dimensional
    auto memspace = dataspace_t(1, &memsize);
    // make a block count
    shape_t count;
    // resize it to the same rank as the requested {shape} and fill it with ones
    // since we read only one block of data
    count.assign(shape.size(), 1);
    // extract the on-disk layout, bridged into an {H5::} dataspace for the selection machinery
    auto filespace = H5::DataSpace(self.dataspace().id());
    // specify the region of interest by selecting the appropriate hyperslab
    filespace.selectHyperslab(H5S_SELECT_SET, &count[0], &origin[0], nullptr, &shape[0]);
    // populate the buffer; {memtype} is a pyre wrapper, so hand over its raw type and space ids
    self.read(memtype.id(), data.data(), memspace.getId(), filespace.getId());
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
    auto memspace = dataspace_t(shape.size(), &shape[0]);
    // make a block count
    shape_t count;
    // resize it to the same rank as the requested {shape} and fill it with ones
    // since we read only one block of data
    count.assign(shape.size(), 1);
    // extract the on-disk layout, bridged into an {H5::} dataspace for the selection machinery
    auto filespace = H5::DataSpace(self.dataspace().id());
    // specify the region of interest by selecting the appropriate hyperslab
    filespace.selectHyperslab(H5S_SELECT_SET, &count[0], &origin[0], nullptr, &shape[0]);
    // populate the buffer; {memtype} is a pyre wrapper, so hand over its raw type and space ids
    self.write(memtype.id(), data.data(), memspace.getId(), filespace.getId());
    // all done
    return;
}

template <class gridT>
auto
pyre::h5::readGrid(
    const dataset_t & self, gridT & data, const datatype_t & memtype, const shape_t & origin,
    const shape_t & shape) -> void
{
    // get my storage
    auto & storage = *data.data();
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
    // get my storage
    auto & storage = *data.data();
    // access the underlying store and delegate
    write(self, storage, memtype, origin, shape);
    // all done
    return;
}


// end of file
