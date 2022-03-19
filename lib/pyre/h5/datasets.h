// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


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
    // and the shape of the block
    const typename gridT::shape_type & shape) -> gridT
{
    // deduce the memory layout description
    const datatype_t & memtype = datatype<typename gridT::value_type>();
    // and delegate
    return read(dataset, memtype, origin, shape);
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
    const typename gridT::shape_type & shape) -> gridT
{
    // alias my grid type and its parts
    using grid_t = gridT;
    using shape_t = typename gridT::shape_type;
    using packing_t = typename gridT::packing_type;
    // alias the {hdf5} dataspace types
    // using h5info_t = hsize_t[shape_t::rank()];
    using h5info_t = std::array<hsize_t, shape_t::rank()>;

    // set up the file data space
    // we need something that converts into {hsize_t} from whatever types {origin}
    // and {shape} use to represent their coordinates
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
    // ask the dataset for a dataspace
    auto fileSpace = dataset.getSpace();
    // select the hyperslab that corresponds to our target region
    fileSpace.selectHyperslab(H5S_SELECT_SET, &count[0], &loc[0]);

    // make a dataspace
    auto memSpace = dataspace_t(shape.rank(), &count[0]);
    // make my grid
    auto grid = grid_t { packing_t(shape), shape.cells() };

    // transfer
    dataset.read(grid.data()->data(), datatype, memSpace, fileSpace);

    // and return the populated grid
    return grid;
}


#endif

// end of file
