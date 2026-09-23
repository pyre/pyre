// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "DCPL.h"
// the reporting of library refusals
#include "../diagnostics.h"
// the fill value methods hand datatypes to the library by id
#include "../types/Datatype.h"


// make a fresh dataset creation property list
pyre::h5::properties::DCPL::DCPL() : OCPL(H5Pcreate(H5P_DATASET_CREATE))
{
    // if the library refused to make it
    if (!valid()) {
        // complain
        complain("pyre.h5.dcpl", "creating a dataset creation property list");
    }
}


// adopt an existing raw handle
pyre::h5::properties::DCPL::DCPL(id_type id) : OCPL(id) {}


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
    if (H5Pget_alloc_time(id(), &timing) < 0) {
        // complain if it refused
        complain("pyre.h5.dcpl", "retrieving the storage allocation time");
        // and report the library default
        return H5D_ALLOC_TIME_DEFAULT;
    }
    // otherwise, report
    return timing;
}


// set the storage allocation time
auto
pyre::h5::properties::DCPL::allocTime(H5D_alloc_time_t timing) -> void
{
    // hand it to the library
    if (H5Pset_alloc_time(id(), timing) < 0) {
        // and complain if it refused
        complain("pyre.h5.dcpl", "setting the storage allocation time");
    }
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
    if (H5Pget_fill_time(id(), &timing) < 0) {
        // complain if it refused
        complain("pyre.h5.dcpl", "retrieving the fill value writing time");
        // and report the library default
        return H5D_FILL_TIME_IFSET;
    }
    // otherwise, report
    return timing;
}


// set the fill value writing time
auto
pyre::h5::properties::DCPL::fillTime(H5D_fill_time_t timing) -> void
{
    // hand it to the library
    if (H5Pset_fill_time(id(), timing) < 0) {
        // and complain if it refused
        complain("pyre.h5.dcpl", "setting the fill value writing time");
    }
    // all done
    return;
}


// the data layout strategy
auto
pyre::h5::properties::DCPL::layout() const -> H5D_layout_t
{
    // the library hands this one back directly
    auto layout = H5Pget_layout(id());
    // if it refused
    if (layout < 0) {
        // complain
        complain("pyre.h5.dcpl", "retrieving the data layout");
        // and report the library default
        return H5D_CONTIGUOUS;
    }
    // otherwise, report
    return layout;
}


// set the data layout strategy
auto
pyre::h5::properties::DCPL::layout(H5D_layout_t layout) -> void
{
    // hand it to the library
    if (H5Pset_layout(id(), layout) < 0) {
        // and complain if it refused
        complain("pyre.h5.dcpl", "setting the data layout");
    }
    // all done
    return;
}


// the chunk shape, given the dataset {rank}
auto
pyre::h5::properties::DCPL::chunk() const -> shape_t
{
    // a dataset that is not chunked has no chunk shape; asking the library for one is an
    // error, so answer from what we know rather than making it complain
    if (layout() != H5D_CHUNKED) {
        // nothing to report
        return {};
    }
    // ask the library how many axes the chunk has
    auto rank = H5Pget_chunk(id(), 0, nullptr);
    // if it could not say
    if (rank < 0) {
        // complain
        complain("pyre.h5.dcpl", "retrieving the rank of the chunk");
        // there is nothing to report
        return {};
    }
    // make a container big enough to hold the answer
    shape_t shape(rank);
    // and fill it; the library will not change its mind between the two calls
    if (H5Pget_chunk(id(), rank, shape.data()) < 0) {
        // unless something is badly wrong
        complain("pyre.h5.dcpl", "retrieving the chunk shape");
        // in which case there is nothing to report
        return {};
    }
    // and report
    return shape;
}


// set the chunk {shape}
auto
pyre::h5::properties::DCPL::chunk(const shape_t & shape) -> void
{
    // hand the rank and extents to the library
    if (H5Pset_chunk(id(), shape.size(), shape.data()) < 0) {
        // and complain if it refused
        complain("pyre.h5.dcpl", "setting the chunk shape");
    }
    // all done
    return;
}


// whether a fill value is defined, and how
auto
pyre::h5::properties::DCPL::fillValueStatus() const -> H5D_fill_value_t
{
    // make room for the answer
    H5D_fill_value_t status = H5D_FILL_VALUE_UNDEFINED;
    // ask the library
    if (H5Pfill_value_defined(id(), &status) < 0) {
        // complain if it refused
        complain("pyre.h5.dcpl", "retrieving the fill value status");
        // and report that none is defined
        return H5D_FILL_VALUE_UNDEFINED;
    }
    // otherwise, hand it off
    return status;
}


// the filters in the dataset pipeline
auto
pyre::h5::properties::DCPL::filters() const -> filters_type
{
    // make a pile
    filters_type pipeline;
    // find out how many filters are registered
    auto count = H5Pget_nfilters(id());
    // if the library refused to say
    if (count < 0) {
        // complain
        complain("pyre.h5.dcpl", "counting the filters in the pipeline");
        // and report an empty pipeline
        return pipeline;
    }
    // go through the registered filters
    for (int i = 0; i < count; ++i) {
        // make some room
        unsigned int flags = 0;
        std::size_t elements = 0;
        char name[256] = "";
        unsigned int configuration = 0;
        // get the info; we do not retrieve the client data, so its buffer is empty
        auto filter =
            H5Pget_filter2(id(), i, &flags, &elements, nullptr, sizeof(name), name, &configuration);
        // if the library refused to describe it
        if (filter < 0) {
            // complain
            complain("pyre.h5.dcpl", "describing filter " + std::to_string(i) + " of the pipeline");
            // and skip it
            continue;
        }
        // store it as something that says what each of its parts is
        pipeline.emplace_back(filter, name, flags, configuration);
    }
    // hand off the pipeline
    return pipeline;
}


// engage the deflate (gzip) filter at the given compression {level}
auto
pyre::h5::properties::DCPL::addDeflate(unsigned int level) -> void
{
    // hand it to the library
    if (H5Pset_deflate(id(), level) < 0) {
        // and complain if it refused
        complain("pyre.h5.dcpl", "setting the deflate filter");
    }
    // all done
    return;
}


// engage the szip filter
auto
pyre::h5::properties::DCPL::addSzip(unsigned int options, unsigned int pixelsPerBlock) -> void
{
    // hand them to the library
    if (H5Pset_szip(id(), options, pixelsPerBlock) < 0) {
        // and complain if it refused
        complain("pyre.h5.dcpl", "setting the szip filter");
    }
    // all done
    return;
}


// engage the n-bit filter
auto
pyre::h5::properties::DCPL::addNbit() -> void
{
    // ask the library
    if (H5Pset_nbit(id()) < 0) {
        // and complain if it refused
        complain("pyre.h5.dcpl", "setting the n-bit filter");
    }
    // all done
    return;
}


// engage the shuffle filter
auto
pyre::h5::properties::DCPL::addShuffle() -> void
{
    // ask the library
    if (H5Pset_shuffle(id()) < 0) {
        // and complain if it refused
        complain("pyre.h5.dcpl", "setting the shuffle filter");
    }
    // all done
    return;
}


// engage the fletcher32 checksum filter
auto
pyre::h5::properties::DCPL::addFletcher32() -> void
{
    // ask the library
    if (H5Pset_fletcher32(id()) < 0) {
        // and complain if it refused
        complain("pyre.h5.dcpl", "setting the fletcher32 filter");
    }
    // all done
    return;
}


// engage the scale-offset filter
auto
pyre::h5::properties::DCPL::addScaleoffset(H5Z_SO_scale_type_t scaleType, int scaleFactor) -> void
{
    // hand the parameters to the library
    if (H5Pset_scaleoffset(id(), scaleType, scaleFactor) < 0) {
        // and complain if it refused
        complain("pyre.h5.dcpl", "setting the scale-offset filter");
    }
    // all done
    return;
}


// end of file
