// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "DataSpace.h"


// make a dataspace of the given {type}
pyre::h5::DataSpace::DataSpace(class_type type) : Identifier(H5Screate(type))
{
    // if the library refused to make it
    if (!valid()) {
        // make a channel
        auto channel = pyre::journal::error_t("pyre.h5.dataspace");
        // and complain
        channel
            // what
            << "failed to create a dataspace of type " << type
            // where
            << pyre::journal::endl(__HERE__);
    }
}


// make a simple dataspace with the given {shape}
pyre::h5::DataSpace::DataSpace(const shape_t & shape) :
    Identifier(H5Screate_simple(shape.size(), shape.data(), nullptr))
{
    // if the library refused to make it
    if (!valid()) {
        // make a channel
        auto channel = pyre::journal::error_t("pyre.h5.dataspace");
        // and complain
        channel
            // what
            << "failed to create a simple dataspace of rank " << shape.size()
            // where
            << pyre::journal::endl(__HERE__);
    }
}


// adopt an existing raw handle
pyre::h5::DataSpace::DataSpace(id_type id) : Identifier(id) {}


// the shared dataspace that denotes the whole extent of a dataset
auto
pyre::h5::DataSpace::all() -> const DataSpace &
{
    // {H5S_ALL} is a sentinel handle, not a live object, so wrapping it is harmless: it never
    // gets reference counted or closed
    static const DataSpace whole { static_cast<id_type>(H5S_ALL) };
    // hand it off
    return whole;
}


// whether i have a simple extent
auto
pyre::h5::DataSpace::simple() const -> bool
{
    // ask the library
    return H5Sis_simple(id()) > 0;
}


// the number of dimensions of my extent
auto
pyre::h5::DataSpace::rank() const -> int
{
    // ask the library
    return H5Sget_simple_extent_ndims(id());
}


// my extent, one entry per dimension
auto
pyre::h5::DataSpace::shape() const -> shape_t
{
    // get my rank
    auto r = rank();
    // if it came back bad
    if (r < 0) {
        // there is no shape to report
        return {};
    }
    // make a correctly sized container
    shape_t extent(r);
    // populate it
    H5Sget_simple_extent_dims(id(), extent.data(), nullptr);
    // and return it
    return extent;
}


// give me a new simple extent
auto
pyre::h5::DataSpace::reshape(const shape_t & shape) -> void
{
    // resize me
    if (H5Sset_extent_simple(id(), shape.size(), shape.data(), nullptr) < 0) {
        // make a channel
        auto channel = pyre::journal::error_t("pyre.h5.dataspace");
        // and complain
        channel
            // what
            << "failed to reshape a dataspace to rank " << shape.size()
            // where
            << pyre::journal::endl(__HERE__);
    }
    // all done
    return;
}


// the number of cells in my extent
auto
pyre::h5::DataSpace::cells() const -> hssize_t
{
    // ask the library
    return H5Sget_simple_extent_npoints(id());
}


// my kind
auto
pyre::h5::DataSpace::type() const -> class_type
{
    // ask the library
    return H5Sget_simple_extent_type(id());
}


// discard my extent, leaving me empty
auto
pyre::h5::DataSpace::clear() -> void
{
    // empty my extent
    H5Sset_extent_none(id());
    // all done
    return;
}


// a copy of me with the same extent and selection
auto
pyre::h5::DataSpace::clone() const -> DataSpace
{
    // copying yields a fresh, owned handle, so the result adopts it
    return DataSpace(static_cast<id_type>(H5Scopy(id())));
}


// release my handle
auto
pyre::h5::DataSpace::close() -> void
{
    // give up my reference; the library closes the object when the last one goes away
    _release();
    // all done
    return;
}


// whether my current selection lies within my extent
auto
pyre::h5::DataSpace::validSelection() const -> bool
{
    // ask the library
    return H5Sselect_valid(id()) > 0;
}


// the (begin, end) bounding box of my current selection
auto
pyre::h5::DataSpace::selectionBounds() const -> slab_t
{
    // get my rank
    auto r = rank();
    // the two corners
    shape_t begin(r < 0 ? 0 : r);
    shape_t end(r < 0 ? 0 : r);
    // hand them to the calculator
    H5Sget_select_bounds(id(), begin.data(), end.data());
    // and return the pair
    return { begin, end };
}


// the number of cells in my current selection
auto
pyre::h5::DataSpace::selectedCells() const -> hssize_t
{
    // ask the library
    return H5Sget_select_npoints(id());
}


// the number of elements in my current point selection
auto
pyre::h5::DataSpace::selectedElements() const -> hssize_t
{
    // ask the library
    return H5Sget_select_elem_npoints(id());
}


// the number of hyperslabs in my current selection
auto
pyre::h5::DataSpace::selectedSlabs() const -> hssize_t
{
    // ask the library
    return H5Sget_select_hyper_nblocks(id());
}


// select my entire extent
auto
pyre::h5::DataSpace::selectAll() -> void
{
    // ask the library
    H5Sselect_all(id());
    // all done
    return;
}


// clear my selection
auto
pyre::h5::DataSpace::selectNone() -> void
{
    // ask the library
    H5Sselect_none(id());
    // all done
    return;
}


// shift my current selection by {delta}
auto
pyre::h5::DataSpace::offset(const offsets_t & delta) -> void
{
    // ask the library
    H5Soffset_simple(id(), delta.data());
    // all done
    return;
}


// combine the given {elements} with my current selection using {op}
auto
pyre::h5::DataSpace::selectElements(selection_type op, const points_t & elements) -> void
{
    // an empty point set is a no-op
    if (elements.empty()) {
        // so there is nothing to do
        return;
    }
    // the number of points, and the dimensionality of each
    auto count = elements.size();
    auto rank = elements.front().size();
    // flatten the coordinates into a single contiguous buffer
    shape_t flat;
    // big enough to hold them all
    flat.reserve(count * rank);
    // go through the points
    for (const auto & point : elements) {
        // and their coordinates
        for (const auto & index : point) {
            // transferring each to the buffer
            flat.push_back(index);
        }
    }
    // combine them with the current selection
    H5Sselect_elements(id(), op, count, flat.data());
    // all done
    return;
}


// the list of selected elements, starting at the {start}-th
auto
pyre::h5::DataSpace::selectedElementList(int start) const -> points_t
{
    // get my rank
    auto r = rank();
    // and the number of selected elements
    auto len = H5Sget_select_elem_npoints(id());
    // if there is nothing to report
    if (r <= 0 || len <= 0) {
        // hand back an empty table
        return {};
    }
    // pull the whole flat coordinate list
    shape_t flat(len * r);
    // populate it
    H5Sget_select_elem_pointlist(id(), 0, len, flat.data());
    // build the coordinate table
    points_t points;
    // go through the requested points
    for (auto p = start; p < len; ++p) {
        // make room for this point's coordinates
        auto & point = points.emplace_back(r);
        // and copy them in
        for (auto index = 0; index < r; ++index) {
            // one coordinate at a time
            point[index] = flat[p * r + index];
        }
    }
    // hand off the table
    return points;
}


// select one slab of the given {shape} at the given {origin}
auto
pyre::h5::DataSpace::slab(const index_t & origin, const shape_t & shape) -> void
{
    // delegate to the general form, replacing the current selection
    slab(H5S_SELECT_SET, origin, shape);
    // all done
    return;
}


// combine one slab of the given {shape} at {origin} with my selection using {op}
auto
pyre::h5::DataSpace::slab(selection_type op, const index_t & origin, const shape_t & shape) -> void
{
    // we want exactly one block per dimension
    shape_t count(shape.size(), 1);
    // each of size {shape}, anchored at {origin}, with no stride
    H5Sselect_hyperslab(id(), op, origin.data(), nullptr, count.data(), shape.data());
    // all done
    return;
}


// combine a fully specified strided slab with my selection using {op}
auto
pyre::h5::DataSpace::slab(
    selection_type op, const shape_t & origin, const shape_t & shape, const shape_t & stride,
    const shape_t & count) -> void
{
    // {shape} gives the per-dimension block size; everything else is passed through
    H5Sselect_hyperslab(id(), op, origin.data(), stride.data(), count.data(), shape.data());
    // all done
    return;
}


// the list of selected hyperslabs, starting at the {start}-th
auto
pyre::h5::DataSpace::selectedSlabList(int start) const -> slabs_t
{
    // get my rank
    auto r = rank();
    // and the number of selected slabs
    auto len = H5Sget_select_hyper_nblocks(id());
    // figure out how many we will extract
    auto blocks = len - start;
    // if there is nothing to report
    if (r <= 0 || blocks <= 0) {
        // hand back an empty list
        return {};
    }
    // each block is stored as a (begin, end) corner pair, so two corners of {r} coordinates
    shape_t flat(2 * r * blocks);
    // populate the buffer, starting at the requested block
    H5Sget_select_hyper_blocklist(id(), start, blocks, flat.data());
    // build the result
    slabs_t slabs;
    // go through the blocks
    for (auto block = 0; block < blocks; ++block) {
        // locate this block in the buffer
        auto cursor = flat.data() + 2 * r * block;
        // the begin corner
        shape_t begin(r);
        // copy it in
        std::copy(cursor, cursor + r, begin.begin());
        // step to the end corner
        cursor += r;
        // the end corner
        shape_t end(r);
        // copy it in
        std::copy(cursor, cursor + r, end.begin());
        // add the pair to the list
        slabs.emplace_back(begin, end);
    }
    // hand off the list
    return slabs;
}


// end of file
