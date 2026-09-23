// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "DataSet.h"
// the reporting of library refusals
#include "diagnostics.h"
// the wrappers i hand back
#include "types/Datatype.h"
#include "Chunk.h"
#include "DataSpace.h"
#include "properties/DAPL.h"
#include "properties/DCPL.h"


// adopt an existing raw handle
pyre::h5::DataSet::DataSet(id_type id) : Location(id) {}


// my full path name within the file
auto
pyre::h5::DataSet::name() const -> string_t
{
    // find out how long my name is
    auto len = H5Iget_name(id(), nullptr, 0);
    // a handle the library will not name, e.g. one that never opened, has no name; this is
    // the caller's answer, and it stays quiet since my name is what complaints are built with
    if (len < 0) {
        // so say so
        return "";
    }
    // make room for it, plus the terminating null
    string_t buffer(len + 1, '\0');
    // retrieve it; the library will not change its mind between the two calls
    if (H5Iget_name(id(), buffer.data(), len + 1) < 0) {
        // unless something is badly wrong
        complain("pyre.h5.dataset", "retrieving the name of a dataset");
        // in which case there is no name
        return "";
    }
    // trim the terminator and report
    buffer.resize(len);
    return buffer;
}


// my on-disk byte offset, if contiguously stored
auto
pyre::h5::DataSet::offset() const -> haddr_t
{
    // ask the library; it answers {HADDR_UNDEF} both when it refuses and when i am not
    // stored contiguously, so the undefined address is the answer, passed through as is
    return H5Dget_offset(id());
}


// the class of my datatype
auto
pyre::h5::DataSet::cell() const -> class_type
{
    // grab my datatype
    auto type = H5Dget_type(id());
    // if the library refused
    if (type < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "retrieving the datatype of '" + name() + "'", reason);
        // and report that there is no class to speak of
        return H5T_NO_CLASS;
    }
    // read its class
    auto cls = H5Tget_class(type);
    // if the library refused
    if (cls == H5T_NO_CLASS) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain(
            "pyre.h5.dataset", "retrieving the class of the datatype of '" + name() + "'", reason);
    }
    // give the temporary type back
    if (H5Tclose(type) < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "releasing the datatype of '" + name() + "'", reason);
    }
    // and report
    return cls;
}


// my datatype, as a fresh owned wrapper
auto
pyre::h5::DataSet::datatype() const -> types::Datatype
{
    // {H5Dget_type} hands back a fresh handle the wrapper adopts
    auto hid = H5Dget_type(id());
    // if the library refused
    if (hid < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "retrieving the datatype of '" + name() + "'", reason);
    }
    // hand off the datatype, empty if the library refused
    return types::Datatype(static_cast<id_type>(hid));
}


// my dataspace, as a fresh owned wrapper
auto
pyre::h5::DataSet::dataspace() const -> DataSpace
{
    // {H5Dget_space} hands back a fresh handle the wrapper adopts
    auto hid = H5Dget_space(id());
    // if the library refused
    if (hid < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "retrieving the dataspace of '" + name() + "'", reason);
    }
    // hand off the dataspace, empty if the library refused
    return DataSpace(static_cast<id_type>(hid));
}


// my extent as a runtime-rank canonical layout, in the {pyre::grid} vocabulary
auto
pyre::h5::DataSet::packing() const -> packing_t
{
    // my dataspace carries my extent, and knows how to speak grid
    return dataspace().packing();
}


// the paired selections that move the chunk at {tile} of a {layout} between my cells and
// its page
auto
pyre::h5::DataSet::_tileSpaces(
    const tiling_t & layout, const tiling_t::index_type & tile, DataSpace & filespace) const
    -> std::optional<DataSpace>
{
    // my extent, in grid vocabulary
    auto extent = filespace.packing().shape();
    // the mosaic addresses a region of me in my own index space, so the ranks must agree
    if (layout.rank() != extent.size()) {
        // anything else is an application error; make a channel
        auto channel = pyre::journal::error_t("pyre.h5.dataset");
        // complain
        channel << pyre::journal::at() << "moving a mosaic of rank " << layout.rank()
                << " through '" << name() << "', a dataset of rank " << extent.size()
                << pyre::journal::endl;
        // and bail
        return std::nullopt;
    }

    // the chunk's own layout, anchored where the chunk lives in the mosaic's index space;
    // an edge chunk keeps its full size, and whatever overhangs my extent is page padding
    auto chunk = layout.tile(tile);
    // room for the clamped file block and for its landing spot within the page
    index_t fileOrigin(layout.rank());
    shape_t fileShape(layout.rank());
    index_t pageOrigin(layout.rank());
    // clamp the chunk against my extent, axis by axis; interior chunks pass through whole
    for (std::size_t axis = 0; axis < layout.rank(); ++axis) {
        // the block begins at the chunk's anchor, but never before my origin
        auto begin = std::max(chunk.origin()[axis], static_cast<tiling_t::difference_type>(0));
        // and ends a full chunk later, but never past my edge
        auto end = std::min(chunk.origin()[axis] + chunk.shape()[axis], extent[axis]);
        // a chunk with nothing inside me holds no cells to move
        if (begin >= end) {
            // so this is an application error; make a channel
            auto channel = pyre::journal::error_t("pyre.h5.dataset");
            // complain
            channel << pyre::journal::at() << "moving a tile that lies outside the extent of '"
                    << name() << "'" << pyre::journal::endl;
            // and bail
            return std::nullopt;
        }
        // the file block starts at the clamped corner, now on the unsigned side
        fileOrigin[axis] = static_cast<hsize_t>(begin);
        // and spans the clamped extent
        fileShape[axis] = static_cast<hsize_t>(end - begin);
        // the block lands at the matching offset within the page
        pageOrigin[axis] = static_cast<hsize_t>(begin - chunk.origin()[axis]);
    }

    // select the file side: the clamped block of my cells
    filespace.slab(fileOrigin, fileShape);
    // describe the memory side: the same block within a page-shaped extent, so that a
    // clipped chunk sits at the right offsets and the page padding is skipped
    auto memspace = DataSpace { shape_t(chunk.shape().begin(), chunk.shape().end()) };
    // by selecting the landing spot
    memspace.slab(pageOrigin, fileShape);
    // hand off the memory space, its selection paired with the one on {filespace}
    return memspace;
}


// my extent diced into my chunks: the tiled layout a mosaic is assembled over
auto
pyre::h5::DataSet::tiling() const -> tiling_t
{
    // my extent, already in grid vocabulary
    auto box = packing().shape();
    // a dataset that is not chunked — contiguous, compact — is stored as a single slab, so
    // its tiling is one tile that covers the whole box; this keeps {tiling} total, and lets
    // readers assemble mosaics over any dataset they encounter
    if (dcpl().layout() != H5D_CHUNKED) {
        // one tile, the box itself
        return tiling_t(box, box);
    }
    // get my chunk shape; it knows its own rank
    auto chunk = dcpl().chunk();
    // the grid vocabulary measures with signed integers; make room for the translation
    tiling_t::shape_type tile(chunk.size());
    // go through the axes
    for (std::size_t axis = 0; axis < chunk.size(); ++axis) {
        // and carry each extent across the signedness boundary
        tile[axis] = static_cast<tiling_t::difference_type>(chunk[axis]);
    }
    // dice my extent into my chunks; edge chunks overhang the box and their overhang is
    // padding, exactly the way hdf5 stores them
    return tiling_t(box, tile);
}


// my on-disk size, in bytes
auto
pyre::h5::DataSet::storageSize() const -> hsize_t
{
    // ask the library; it answers zero both when it refuses and when nothing has been
    // written, so zero is the answer, passed through as is
    return H5Dget_storage_size(id());
}


// my in-memory size, in bytes
auto
pyre::h5::DataSet::memorySize() const -> std::size_t
{
    // my number of elements comes from my dataspace
    auto space = H5Dget_space(id());
    // if the library refused
    if (space < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "retrieving the dataspace of '" + name() + "'", reason);
        // and report that i occupy nothing
        return 0;
    }
    // count the elements
    auto points = H5Sget_simple_extent_npoints(space);
    // if the library refused
    if (points < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "counting the cells of '" + name() + "'", reason);
        // and there is nothing to count
        points = 0;
    }
    // give the temporary space back
    if (H5Sclose(space) < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "releasing the dataspace of '" + name() + "'", reason);
    }
    // the size of each comes from my datatype
    auto type = H5Dget_type(id());
    // if the library refused
    if (type < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "retrieving the datatype of '" + name() + "'", reason);
        // and report that i occupy nothing
        return 0;
    }
    // measure a cell; the library answers zero when it refuses, and no cell is that small
    auto size = H5Tget_size(type);
    // so zero means it refused
    if (size == 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "measuring the cells of '" + name() + "'", reason);
    }
    // give the temporary type back
    if (H5Tclose(type) < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "releasing the datatype of '" + name() + "'", reason);
    }
    // the total is the product
    return static_cast<std::size_t>(points) * size;
}


// how many chunks i hold
auto
pyre::h5::DataSet::chunks() const -> std::optional<hsize_t>
{
    // the chunk table only exists for datasets that are stored as chunks; the library
    // rejects the question for any other layout, so screen it here rather than let an
    // error stack unwind at the caller
    if (dcpl().layout() != H5D_CHUNKED) {
        // there is no table to count
        return {};
    }
    // make room for the answer
    hsize_t count = 0;
    // ask the library about the whole of me, rather than some selected part
    auto status = H5Dget_num_chunks(id(), H5S_ALL, &count);
    // if the library balked
    if (status < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "counting the chunks of '" + name() + "'", reason);
        // and decline to answer
        return {};
    }
    // hand back the tally
    return count;
}


// the chunk at {index} of my table
auto
pyre::h5::DataSet::chunk(hsize_t index) const -> std::optional<Chunk>
{
    // find out how many chunks there are to walk; this also screens out the layouts that
    // have no chunk table at all
    auto total = chunks();
    // if there is no table
    if (!total) {
        // there is nothing at any index
        return {};
    }
    // an index past the end is a caller mistake, and one worth naming: the library would
    // reject it too, but silently, and the table shrinks and grows as chunks are written
    if (index >= *total) {
        // make a channel
        auto channel = pyre::journal::error_t("pyre.h5");
        // complain
        channel << "while looking up chunk " << index << " of '" << name() << "'"
                << pyre::journal::newline << "only " << *total << " chunks have been written"
                << pyre::journal::endl(__HERE__);
        // and decline to answer
        return {};
    }
    // make room for the origin, one coordinate per axis of my extent
    auto origin = index_t(packing().rank(), 0);
    // and for the rest of what the library reports
    unsigned int filterMask = 0;
    haddr_t address = 0;
    hsize_t bytes = 0;
    // ask
    auto status =
        H5Dget_chunk_info(id(), H5S_ALL, index, origin.data(), &filterMask, &address, &bytes);
    // if the library balked
    if (status < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain(
            "pyre.h5.dataset", "looking up chunk " + std::to_string(index) + " of '" + name() + "'",
            reason);
        // and decline to answer
        return {};
    }
    // assemble the description
    return Chunk(origin, filterMask, address, bytes);
}


// the corner of the chunk that holds the cell at {origin}
auto
pyre::h5::DataSet::_corner(const index_t & origin) const -> std::optional<index_t>
{
    // there are no chunks to speak of unless i am stored as chunks
    if (dcpl().layout() != H5D_CHUNKED) {
        // so there is no corner to hand back
        return {};
    }
    // my extent, which the cell has to lie inside
    auto box = packing().shape();
    // a cell of the wrong rank cannot be checked, let alone used
    if (origin.size() != box.size()) {
        // make a channel
        auto channel = pyre::journal::error_t("pyre.h5");
        // complain
        channel << "while looking for the chunk of '" << name() << "' at a given cell"
                << pyre::journal::newline << "the cell has " << origin.size()
                << " coordinates, but the dataset has rank " << box.size()
                << pyre::journal::endl(__HERE__);
        // and decline to answer
        return {};
    }
    // my chunk shape, which says where the corners fall
    auto chunk = dcpl().chunk();
    // make room for the corner
    auto corner = index_t(origin.size(), 0);
    // go through the axes
    for (std::size_t axis = 0; axis < origin.size(); ++axis) {
        // the library does not bounds check the calls this feeds: an impossible cell comes
        // back looking exactly like a chunk nobody ever wrote, so check here or the two
        // answers become indistinguishable
        if (origin[axis] >= static_cast<hsize_t>(box[axis])) {
            // make a channel
            auto channel = pyre::journal::error_t("pyre.h5");
            // complain
            channel << "while looking for the chunk of '" << name() << "' at a given cell"
                    << pyre::journal::newline << "coordinate " << axis << " is " << origin[axis]
                    << ", which is outside my extent of " << box[axis]
                    << pyre::journal::endl(__HERE__);
            // and decline to answer
            return {};
        }
        // otherwise, round the coordinate down to the nearest multiple of the chunk extent
        corner[axis] = origin[axis] - origin[axis] % chunk[axis];
    }
    // hand back the anchor of the chunk that holds the cell
    return corner;
}


// the chunk that holds the cell at {origin}
auto
pyre::h5::DataSet::chunkAt(const index_t & origin) const -> std::optional<Chunk>
{
    // work out which chunk the cell belongs to; this screens the layout, the rank, and the
    // bounds, and has already complained if any of them was wrong
    auto corner = _corner(origin);
    // if there is no such chunk
    if (!corner) {
        // there is nothing to describe
        return {};
    }
    // make room for what the library reports
    unsigned int filterMask = 0;
    haddr_t address = 0;
    hsize_t bytes = 0;
    // ask; this call takes any cell of a chunk, so the snapped corner suits it fine
    auto status = H5Dget_chunk_info_by_coord(id(), corner->data(), &filterMask, &address, &bytes);
    // if the library balked
    if (status < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain(
            "pyre.h5.dataset", "looking for the chunk of '" + name() + "' at a given cell", reason);
        // and decline to answer
        return {};
    }
    // a chunk nobody has written has no address; that is not a failure, it is the answer,
    // and it says the region is pure fill
    if (address == HADDR_UNDEF) {
        // report the absence
        return {};
    }
    // assemble the description, anchored at the chunk's own corner rather than at the cell
    // the caller happened to probe with
    return Chunk(*corner, filterMask, address, bytes);
}


// read the chunk that holds the cell at {origin} in its stored form
auto
pyre::h5::DataSet::readChunk(const index_t & origin, bytes_t & buffer) const
    -> std::optional<unsigned int>
{
    // find out whether there is a chunk there at all, and how much room its stored form
    // needs; this screens the layout, the rank and the bounds on our behalf
    auto chunk = chunkAt(origin);
    // a chunk that was never written has no bytes to hand over
    if (!chunk) {
        // so say so; this is the answer, not a failure
        return {};
    }
    // size the destination from what the library says the chunk occupies, so that the
    // caller cannot get it wrong and the read cannot run past the end of the buffer
    buffer.resize(chunk->bytes);
    // make room for the mask of filters the chunk was spared
    uint32_t filterMask = 0;
    // the direct read insists on the chunk's own corner, unlike the table lookup above,
    // which is why the corner rather than the caller's cell goes in here
#if H5_VERSION_GE(2, 0, 0)
    // hdf5 2.0 takes the room available and reports the bytes it used, so the buffer is
    // guarded by the library as well as by us
    auto room = buffer.size();
    auto status =
        H5Dread_chunk(id(), H5P_DEFAULT, chunk->origin.data(), &filterMask, buffer.data(), &room);
#else
    // older libraries take the caller's word for it, which is safe here only because the
    // buffer was sized from the chunk's own storage size a moment ago
    auto status =
        H5Dread_chunk(id(), H5P_DEFAULT, chunk->origin.data(), &filterMask, buffer.data());
#endif
    // if the library balked
    if (status < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain(
            "pyre.h5.dataset", "reading a chunk of '" + name() + "' in its stored form", reason);
        // leave nothing misleading behind
        buffer.clear();
        // and decline to answer
        return {};
    }
    // hand back the filters this chunk was spared, which is what a caller needs in order to
    // lay these same bytes down somewhere else
    return filterMask;
}


// lay {buffer} down as the chunk that holds the cell at {origin}
auto
pyre::h5::DataSet::writeChunk(
    const index_t & origin, unsigned int filterMask, const bytes_t & buffer) const -> void
{
    // work out which chunk the cell belongs to; the direct write insists on the chunk's own
    // corner, and this screens the layout, the rank and the bounds besides
    auto corner = _corner(origin);
    // if there is no such chunk
    if (!corner) {
        // the complaint has already been lodged, so just stop
        return;
    }
    // hand the bytes over exactly as they are; nothing is converted, selected, or filtered
    // on the way in, so whatever the caller supplies is what ends up in the file
    auto status =
        H5Dwrite_chunk(id(), H5P_DEFAULT, filterMask, corner->data(), buffer.size(), buffer.data());
    // if the library balked
    if (status < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain(
            "pyre.h5.dataset", "writing a chunk of '" + name() + "' in its stored form", reason);
        // and bail
        return;
    }
    // all done
    return;
}


// my access property list, as a fresh owned wrapper
auto
pyre::h5::DataSet::dapl() const -> properties::DAPL
{
    // {H5Dget_access_plist} hands back a fresh handle the wrapper adopts
    auto hid = H5Dget_access_plist(id());
    // if the library refused
    if (hid < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain(
            "pyre.h5.dataset", "retrieving the access property list of '" + name() + "'", reason);
    }
    // hand off the list, empty if the library refused
    return properties::DAPL(static_cast<id_type>(hid));
}


// my creation property list, as a fresh owned wrapper
auto
pyre::h5::DataSet::dcpl() const -> properties::DCPL
{
    // {H5Dget_create_plist} hands back a fresh handle the wrapper adopts
    auto hid = H5Dget_create_plist(id());
    // if the library refused
    if (hid < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain(
            "pyre.h5.dataset", "retrieving the creation property list of '" + name() + "'", reason);
    }
    // hand off the list, empty if the library refused
    return properties::DCPL(static_cast<id_type>(hid));
}


// fill {buffer}, interpreted as {memtype}, from the selected region
auto
pyre::h5::DataSet::read(
    id_type memtype, void * buffer, id_type memspace, id_type filespace, id_type dxpl) const -> void
{
    // hand it to the library, along with whatever the caller wants done to the cells in
    // flight; {dxpl} is the only place a data transform or a transfer buffer can be named
    if (H5Dread(id(), memtype, memspace, filespace, dxpl, buffer) < 0) {
        // and complain if it refused
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "reading the selected region of '" + name() + "'", reason);
    }
    // all done
    return;
}


// write {buffer}, interpreted as {memtype}, into the selected region
auto
pyre::h5::DataSet::write(
    id_type memtype, const void * buffer, id_type memspace, id_type filespace, id_type dxpl) const
    -> void
{
    // hand it to the library, along with whatever the caller wants done to the cells in
    // flight; {dxpl} is the only place a data transform or a transfer buffer can be named
    if (H5Dwrite(id(), memtype, memspace, filespace, dxpl, buffer) < 0) {
        // and complain if it refused
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "writing the selected region of '" + name() + "'", reason);
    }
    // all done
    return;
}


// read my contents as a string, trimming the persisted padding
auto
pyre::h5::DataSet::readString(id_type memspace, id_type filespace) const -> string_t
{
    // grab my datatype
    auto type = H5Dget_type(id());
    // if the library refused
    if (type < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "retrieving the datatype of '" + name() + "'", reason);
        // and there is no string to read
        return "";
    }
    // find out whether i hold variable length strings
    auto variable = H5Tis_variable_str(type);
    // if the library would not say
    if (variable < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "inspecting the string type of '" + name() + "'", reason);
        // give the temporary type back
        if (H5Tclose(type) < 0) {
            // the library's reasons, before asking it for my name disturbs them
            auto reason = explanation();
            // and complain
            complain("pyre.h5.dataset", "releasing the datatype of '" + name() + "'", reason);
        }
        // and there is no string to read
        return "";
    }
    // variable length strings come back as a library-allocated pointer
    if (variable > 0) {
        // make room for the pointer
        char * raw = nullptr;
        // read it
        if (H5Dread(id(), type, memspace, filespace, H5P_DEFAULT, &raw) < 0) {
            // complaining if the library refused; the pointer stays null and the string empty
            // the library's reasons, before asking it for my name disturbs them
            auto reason = explanation();
            // and complain
            complain("pyre.h5.dataset", "reading the string in '" + name() + "'", reason);
        }
        // copy it into a managed string
        string_t value(raw ? raw : "");
        // give the library's buffer back
        if (H5free_memory(raw) < 0) {
            // the library's reasons, before asking it for my name disturbs them
            auto reason = explanation();
            // and complain
            complain("pyre.h5.dataset", "releasing the string buffer of '" + name() + "'", reason);
        }
        // release the temporary type
        if (H5Tclose(type) < 0) {
            // the library's reasons, before asking it for my name disturbs them
            auto reason = explanation();
            // and complain
            complain("pyre.h5.dataset", "releasing the datatype of '" + name() + "'", reason);
        }
        // and report; variable length strings carry no padding to trim
        return value;
    }
    // fixed length strings come back inline; remember how they are padded
    auto pad = H5Tget_strpad(type);
    // if the library would not say
    if (pad == H5T_STR_ERROR) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain(
            "pyre.h5.dataset", "retrieving the padding of the strings in '" + name() + "'", reason);
    }
    // measure the stored string; the library answers zero when it refuses
    auto size = H5Tget_size(type);
    // so zero means it refused
    if (size == 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "measuring the strings in '" + name() + "'", reason);
    }
    // make a buffer the right size
    string_t value(size, '\0');
    // read into it
    if (H5Dread(id(), type, memspace, filespace, H5P_DEFAULT, value.data()) < 0) {
        // complaining if the library refused; the buffer stays blank
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "reading the string in '" + name() + "'", reason);
    }
    // release the temporary type
    if (H5Tclose(type) < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "releasing the datatype of '" + name() + "'", reason);
    }
    // trim the padding and report
    _trim(value, pad);
    return value;
}


// write {value} into me as a string
auto
pyre::h5::DataSet::writeString(const string_t & value, id_type memspace, id_type filespace) const
    -> void
{
    // grab my datatype
    auto type = H5Dget_type(id());
    // if the library refused
    if (type < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "retrieving the datatype of '" + name() + "'", reason);
        // and there is nowhere to write
        return;
    }
    // find out whether i hold variable length strings
    auto variable = H5Tis_variable_str(type);
    // if the library would not say
    if (variable < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "inspecting the string type of '" + name() + "'", reason);
        // give the temporary type back
        if (H5Tclose(type) < 0) {
            // the library's reasons, before asking it for my name disturbs them
            auto reason = explanation();
            // and complain
            complain("pyre.h5.dataset", "releasing the datatype of '" + name() + "'", reason);
        }
        // and there is nowhere to write
        return;
    }
    // variable length strings go out as a pointer to the contents
    if (variable > 0) {
        // the library copies from the address i hand it
        const char * raw = value.data();
        // write it
        if (H5Dwrite(id(), type, memspace, filespace, H5P_DEFAULT, &raw) < 0) {
            // complaining if the library refused
            // the library's reasons, before asking it for my name disturbs them
            auto reason = explanation();
            // and complain
            complain("pyre.h5.dataset", "writing the string in '" + name() + "'", reason);
        }
        // release the temporary type
        if (H5Tclose(type) < 0) {
            // the library's reasons, before asking it for my name disturbs them
            auto reason = explanation();
            // and complain
            complain("pyre.h5.dataset", "releasing the datatype of '" + name() + "'", reason);
        }
        // all done
        return;
    }
    // measure the stored string; the library answers zero when it refuses
    auto size = H5Tget_size(type);
    // so zero means it refused
    if (size == 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "measuring the strings in '" + name() + "'", reason);
    }
    // fixed length strings go out inline; pad the value out to the stored size
    string_t buffer = value;
    buffer.resize(size, '\0');
    // write it
    if (H5Dwrite(id(), type, memspace, filespace, H5P_DEFAULT, buffer.data()) < 0) {
        // complaining if the library refused
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "writing the string in '" + name() + "'", reason);
    }
    // release the temporary type
    if (H5Tclose(type) < 0) {
        // the library's reasons, before asking it for my name disturbs them
        auto reason = explanation();
        // and complain
        complain("pyre.h5.dataset", "releasing the datatype of '" + name() + "'", reason);
    }
    // all done
    return;
}


// release my handle
auto
pyre::h5::DataSet::close() -> void
{
    // give up my reference; the library closes the dataset when the last one goes away
    _release();
    // all done
    return;
}


// trim the persisted padding from {value} according to the string padding strategy {pad}
auto
pyre::h5::DataSet::_trim(string_t & value, H5T_str_t pad) const -> void
{
    // deduce the terminator from the padding method
    switch (pad) {
        // null padded or null terminated strings end at the first null
        case H5T_STR_NULLPAD:
        case H5T_STR_NULLTERM: {
            // find the first null
            auto stop = value.find('\0');
            // and drop everything from there on, if any
            if (stop != string_t::npos) {
                value.resize(stop);
            }
            break;
        }
        // fortran style strings are padded on the right with spaces
        case H5T_STR_SPACEPAD: {
            // find the last non-space
            auto stop = value.find_last_not_of(' ');
            // and keep up to and including it
            value.resize(stop == string_t::npos ? 0 : stop + 1);
            break;
        }
        // anything else is a bug: hdf5 has added a method we don't know about
        default: {
            auto channel = pyre::journal::firewall_t("pyre.h5.dataset");
            channel
                // what
                << "unknown string padding method "
                << pad
                // where
                << pyre::journal::endl(__HERE__);
            break;
        }
    }
    // all done
    return;
}


// end of file
