// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "DCPL.h"


// make a fresh dataset creation property list
pyre::h5::properties::DCPL::DCPL() : List(H5Pcreate(H5P_DATASET_CREATE)) {}


// adopt an existing raw handle
pyre::h5::properties::DCPL::DCPL(id_type id) : List(id) {}


// the shared default dataset creation property list
auto
pyre::h5::properties::DCPL::theDefault() -> const DCPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const DCPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


// the storage allocation time
auto
pyre::h5::properties::DCPL::allocTime() const -> H5D_alloc_time_t
{
    // make room for the answer
    H5D_alloc_time_t timing = H5D_ALLOC_TIME_DEFAULT;
    // ask the library
    H5Pget_alloc_time(id(), &timing);
    // and report
    return timing;
}


// set the storage allocation time
auto
pyre::h5::properties::DCPL::setAllocTime(H5D_alloc_time_t timing) -> void
{
    // hand it to the library
    H5Pset_alloc_time(id(), timing);
    // all done
    return;
}


// the fill value writing time
auto
pyre::h5::properties::DCPL::fillTime() const -> H5D_fill_time_t
{
    // make room for the answer
    H5D_fill_time_t timing = H5D_FILL_TIME_IFSET;
    // ask the library
    H5Pget_fill_time(id(), &timing);
    // and report
    return timing;
}


// set the fill value writing time
auto
pyre::h5::properties::DCPL::setFillTime(H5D_fill_time_t timing) -> void
{
    // hand it to the library
    H5Pset_fill_time(id(), timing);
    // all done
    return;
}


// the data layout strategy
auto
pyre::h5::properties::DCPL::layout() const -> H5D_layout_t
{
    // the library hands this one back directly
    return H5Pget_layout(id());
}


// set the data layout strategy
auto
pyre::h5::properties::DCPL::setLayout(H5D_layout_t layout) -> void
{
    // hand it to the library
    H5Pset_layout(id(), layout);
    // all done
    return;
}


// the chunk shape, given the dataset {rank}
auto
pyre::h5::properties::DCPL::chunk(int rank) const -> shape_t
{
    // make a container big enough to hold the answer
    shape_t shape(rank < 0 ? 0 : rank);
    // ask the library
    H5Pget_chunk(id(), rank, shape.data());
    // and report
    return shape;
}


// set the chunk {shape}
auto
pyre::h5::properties::DCPL::setChunk(const shape_t & shape) -> void
{
    // hand the rank and extents to the library
    H5Pset_chunk(id(), shape.size(), shape.data());
    // all done
    return;
}


// the filters in the dataset pipeline
auto
pyre::h5::properties::DCPL::filters() const -> filters_type
{
    // make a pile
    filters_type pipeline;
    // go through the registered filters
    for (int i = 0; i < H5Pget_nfilters(id()); ++i) {
        // make some room
        unsigned int flags = 0;
        std::size_t elements = 0;
        char name[256];
        unsigned int configuration = 0;
        // get the info; we do not retrieve the client data, so its buffer is empty
        auto filter =
            H5Pget_filter2(id(), i, &flags, &elements, nullptr, sizeof(name), name, &configuration);
        // store it
        pipeline.emplace_back(filter, name, flags, configuration);
    }
    // hand off the pipeline
    return pipeline;
}


// engage the deflate (gzip) filter at the given compression {level}
auto
pyre::h5::properties::DCPL::setDeflate(unsigned int level) -> void
{
    // hand it to the library
    H5Pset_deflate(id(), level);
    // all done
    return;
}


// engage the szip filter
auto
pyre::h5::properties::DCPL::setSzip(unsigned int options, unsigned int pixelsPerBlock) -> void
{
    // hand them to the library
    H5Pset_szip(id(), options, pixelsPerBlock);
    // all done
    return;
}


// engage the n-bit filter
auto
pyre::h5::properties::DCPL::setNbit() -> void
{
    // ask the library
    H5Pset_nbit(id());
    // all done
    return;
}


// engage the shuffle filter
auto
pyre::h5::properties::DCPL::setShuffle() -> void
{
    // ask the library
    H5Pset_shuffle(id());
    // all done
    return;
}


// engage the fletcher32 checksum filter
auto
pyre::h5::properties::DCPL::setFletcher32() -> void
{
    // ask the library
    H5Pset_fletcher32(id());
    // all done
    return;
}


// engage the scale-offset filter
auto
pyre::h5::properties::DCPL::setScaleoffset(H5Z_SO_scale_type_t scaleType, int scaleFactor) -> void
{
    // hand the parameters to the library
    H5Pset_scaleoffset(id(), scaleType, scaleFactor);
    // all done
    return;
}


// end of file
