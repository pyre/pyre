// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// set up the namespace
#include "forward.h"
// my base class
#include "Location.h"
// the dataspaces my mosaic machinery builds and selects over
#include "DataSpace.h"


// an hdf5 dataset
class pyre::h5::DataSet : public pyre::h5::Location {
    // types
public:
    // me
    using self_type = DataSet;
    // my superclass
    using super_type = pyre::h5::Location;
    // the class of my datatype: integer, float, string, ...
    using class_type = H5T_class_t;

    // metamethods
public:
    // adopt an existing raw handle, e.g. one returned by the c api
    explicit DataSet(id_type id);
    // the full set of special members
    DataSet(const DataSet &) = default;
    DataSet(DataSet &&) noexcept = default;
    DataSet & operator=(const DataSet &) = default;
    DataSet & operator=(DataSet &&) noexcept = default;
    ~DataSet() override = default;

    // interface
public:
    // my full path name within the file
    auto name() const -> string_t;
    // my on-disk byte offset, if contiguously stored
    auto offset() const -> haddr_t;
    // the class of my datatype
    auto cell() const -> class_type;
    // my datatype, as a fresh owned wrapper
    auto datatype() const -> types::Datatype;
    // my dataspace, as a fresh owned wrapper
    auto dataspace() const -> DataSpace;
    // my extent as a runtime-rank canonical layout, in the {pyre::grid} vocabulary
    auto packing() const -> packing_t;
    // my extent diced into my chunks: the tiled layout a mosaic is assembled over; a
    // dataset that is not chunked is a single slab, described as one tile covering its
    // whole extent
    auto tiling() const -> tiling_t;
    // an out-of-core mosaic assembled over my own chunking: my tiled layout married to a
    // store with one demand-materialized page per chunk; describing me costs a page table
    // and nothing more, no matter my extent, and the caller names the cell type since the
    // receiving code must allocate for it
    template <class cellT>
    auto mosaic() const -> mosaic_t<cellT>;
    // the smallest mosaic that covers a window: its box is the chunk-aligned cover of the
    // window with the given anchor and extent, so it holds one page per touched chunk and
    // addresses my own index space
    template <class cellT>
    auto mosaic(const tiling_t::index_type & base, const tiling_t::shape_type & extent) const
        -> mosaic_t<cellT>;

    // make an entire {mosaic} resident: pull every chunk of its box into its page; this is
    // the no-ceremony path for algorithms that cannot work on partial results
    template <class cellT>
    auto fill(const mosaic_t<cellT> & mosaic) const -> void;
    // pull the chunk at {tile} of a {mosaic} into its page: materialize the page, land the
    // cells clamped against my extent, and record the deposit; this is the seam where an
    // algorithm that can process partial results interleaves its work with the i/o
    template <class cellT>
    auto fill(const mosaic_t<cellT> & mosaic, const tiling_t::index_type & tile) const -> void;

    // make me agree with a {mosaic}: push every page that is resident and has diverged back
    // into the file; pages the producer never touched, or that already match, are skipped
    template <class cellT>
    auto flush(const mosaic_t<cellT> & mosaic) const -> void;
    // push the chunk at {tile} of a {mosaic} back into the file, clamped against my extent,
    // and record that the page matches me again; the tile's page must be resident
    template <class cellT>
    auto flush(const mosaic_t<cellT> & mosaic, const tiling_t::index_type & tile) const -> void;
    // my on-disk size, in bytes
    auto storageSize() const -> hsize_t;
    // my in-memory size, in bytes
    auto memorySize() const -> std::size_t;

    // the chunk table: which of the chunks my tiling describes have actually been written
    // how many chunks i hold; nothing at all when i am not stored as chunks, which is a
    // different answer from being chunked with nothing written into me yet
    auto chunks() const -> std::optional<hsize_t>;
    // the chunk at {index} of my table; the table lists only the chunks that exist, in the
    // logical order of their origins, so an index is a cursor and not a durable address:
    // writing a chunk that sorts earlier renumbers everything behind it
    auto chunk(hsize_t index) const -> std::optional<Chunk>;
    // the chunk that holds the cell at {origin}; any cell of a chunk names it, not just its
    // corner. nothing comes back when that chunk has never been written, which is the cheap
    // way to know a region is pure fill and not worth reading
    auto chunkAt(const index_t & origin) const -> std::optional<Chunk>;
    // my access property list, as a fresh owned wrapper
    auto dapl() const -> properties::DAPL;
    // my creation property list, as a fresh owned wrapper
    auto dcpl() const -> properties::DCPL;

    // the value that stands in for my cells nobody ever wrote, or nothing when i was made
    // without one. this is the only place the question is well posed: a fill value has no
    // type of its own, since hdf5 converts it to mine when i am created, so i am the one
    // who knows how to read it back. naming {valueT} says what the caller expects to get,
    // and i refuse rather than reinterpret when that disagrees with what i hold
    template <class valueT>
    auto fillValue() const -> std::optional<valueT>;

    // raw value access; {memspace}/{filespace} default to the whole extent
    // fill {buffer}, interpreted as {memtype}, from the selected region
    auto read(
        id_type memtype, void * buffer, id_type memspace = H5S_ALL,
        id_type filespace = H5S_ALL) const -> void;
    // write {buffer}, interpreted as {memtype}, into the selected region
    auto write(
        id_type memtype, const void * buffer, id_type memspace = H5S_ALL,
        id_type filespace = H5S_ALL) const -> void;
    // read my contents as a string, trimming the persisted padding
    auto readString(id_type memspace = H5S_ALL, id_type filespace = H5S_ALL) const -> string_t;
    // write {value} into me as a string
    auto writeString(
        const string_t & value, id_type memspace = H5S_ALL, id_type filespace = H5S_ALL) const
        -> void;

    // release my handle
    auto close() -> void;

    // implementation details
private:
    // trim the persisted padding from {value} according to the string padding strategy {pad}
    auto _trim(string_t & value, H5T_str_t pad) const -> void;
    // assemble a mosaic over a tiled {layout}: one demand-materialized page per tile
    template <class cellT>
    auto _assemble(const tiling_t & layout) const -> mosaic_t<cellT>;
    // the paired selections that move the chunk at {tile} of a {layout} between my cells
    // and its page: select the clamped block on {filespace} and hand back the matching
    // page-shaped memory space; an empty answer means the geometry is unusable, and the
    // complaint has already been lodged
    auto _tileSpaces(
        const tiling_t & layout, const tiling_t::index_type & tile, DataSpace & filespace) const
        -> std::optional<DataSpace>;
};


// the inline implementations
#include "DataSet.icc"


// end of file
