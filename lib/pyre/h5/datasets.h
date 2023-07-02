// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// code guard
#if !defined(pyre_h5_datasets_h)
#define pyre_h5_datasets_h


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
    const typename gridT::shape_type & strides) -> gridT
{
    // deduce the memory layout description
    const datatype_t & memtype = datatype<typename gridT::value_type>();
    // and delegate
    return read(dataset, memtype, origin, shape, strides);
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
    const typename gridT::shape_type & strides) -> gridT
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
    std::transform(strides.begin(), strides.end(), skip.begin(), cast);
    // ask the dataset for a dataspace
    auto fileSpace = dataset.getSpace();
    // select the hyperslab that corresponds to our target region
    fileSpace.selectHyperslab(H5S_SELECT_SET, &count[0], &loc[0], &skip[0]);

    // make a dataspace
    auto memSpace = dataspace_t(shape.rank(), &count[0]);
    // make my grid
    auto grid = grid_t { packing_t(shape), shape.cells() };

    // attempt to
    try {
        // read the data into my {grid}
        dataset.read(grid.data()->data(), datatype, memSpace, fileSpace);
    }
    // if something goes wrong
    catch (const H5::Exception & error) {
        // make a channel
        auto channel = pyre::journal::error_t("pyre.h5.read");
        // and complain
        channel
            // the error
            << "error: " << error.getDetailMsg()
            << pyre::journal::newline
            // shape
            << "while reading a (" << shape << ") tile from (" << origin << ") with strides ("
            << strides << ")"
            << pyre::journal::newline
            // dataset
            << "from the dataset '" << dataset.getObjName()
            << "'"
            // flush
            << pyre::journal::endl(__HERE__);
    }

    // if all goes well, return the populated grid
    return grid;
}

// generics
template <class memT>
auto
pyre::h5::read(
    const dataset_t & self, memT & data, const datatype_t & memtype, const shape_t & origin,
    const shape_t shape) -> void
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
    // extract the on-disk layout
    auto filespace = self.getSpace();
    // specify the region of interest by selecting the appropriate hyperslab
    filespace.selectHyperslab(H5S_SELECT_SET, &count[0], &origin[0], nullptr, &shape[0]);
    // populate the buffer
    self.read(data.data(), memtype, memspace, filespace);
    // all done
    return;
}

template <class memT>
auto
pyre::h5::write(
    const dataset_t & self, memT & data, const datatype_t & memtype, const shape_t & origin,
    const shape_t shape) -> void
{
    // pretend the memory buffer is the same shape as the incoming tile
    auto memspace = dataspace_t(shape.size(), &shape[0]);
    // make a block count
    shape_t count;
    // resize it to the same rank as the requested {shape} and fill it with ones
    // since we read only one block of data
    count.assign(shape.size(), 1);
    // extract the on-disk layout
    auto filespace = self.getSpace();
    // specify the region of interest by selecting the appropriate hyperslab
    filespace.selectHyperslab(H5S_SELECT_SET, &count[0], &origin[0], nullptr, &shape[0]);
    // populate the buffer
    self.write(data.data(), memtype, memspace, filespace);
    // all done
    return;
}

template <class gridT>
auto
pyre::h5::writeGrid(
    const dataset_t & self, gridT & data, const datatype_t & memtype, const shape_t & origin,
    const shape_t shape) -> void
{
    // get my storage
    auto & storage = *data.data();
    // access the underlying store and delegate
    write(self, storage, memtype, origin, shape);
    // all done
    return;
}


#endif

// end of file
