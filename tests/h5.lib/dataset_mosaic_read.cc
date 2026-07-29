// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// for the cleanup of the scratch product
#include <cstdio>
// get the h5 support
#include <pyre/h5.h>
// and the storage strategies a mosaic is assembled over
#include <pyre/memory.h>


// the exhibit: the out-of-core read
//
// an algorithm wants a window of a large chunked product; the recipe reads only the chunks
// the window touches, lands each one in its own page with no intermediate copies, and hands
// the algorithm a mosaic it can address in the product's own index space
//
// the recipe, in five steps:
//   1. let the dataset describe itself: {tiling()} is the product diced into its chunks
//   2. assemble a mosaic over the full description; this is free: nothing is resident
//   3. ask {tilesOverlapping} which chunks the window touches
//   4. for each touched chunk: materialize its page and read the chunk into it
//   5. the algorithm reads the window through the mosaic, unaware it is out-of-core

// the cell type of the product; this is the one thing the recipe fixes at compile time,
// since the code that receives the data must name the type in order to allocate for it
using cell_t = double;
// the storage side of the mosaic: one demand-materialized page per chunk
using paged_t = pyre::memory::paged_t<cell_t>;
// and the mosaic itself: the dataset's own tiled layout married to the paged storage
using mosaic_t = pyre::grid::grid_t<pyre::h5::tiling_t, paged_t>;

// the recognizable content of the product
static auto
stamp(std::ptrdiff_t row, std::ptrdiff_t col) -> cell_t
{
    // a value that encodes its own coordinates
    return static_cast<cell_t>(100 * row + col);
}


// exercise the recipe against a scratch product
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dataset_mosaic_read");

    // the scratch product
    auto uri = "dataset_mosaic_read.h5";

    // the setup, playing the role of whoever produced the data: a 100x100 product, diced
    // into 30x40 chunks so that the edge chunks overhang the extent and the read side has
    // to cope with partial chunks
    {
        // make the file
        pyre::h5::File file { uri, H5F_ACC_TRUNC, {}, {} };
        // describe the extent
        pyre::h5::DataSpace space { pyre::h5::shape_t { 100, 100 } };
        // and the chunking
        pyre::h5::properties::DCPL dcpl;
        // deliberately not a divisor of the extent along either axis
        dcpl.setChunk(pyre::h5::shape_t { 30, 40 });
        // make the dataset
        auto dataset = file.createDataSet(
            "product", pyre::h5::datatype<cell_t>(), space, dcpl, pyre::h5::properties::DAPL());
        // room for the content
        std::vector<cell_t> content(100 * 100);
        // fill every cell with a value that encodes its own coordinates
        for (std::ptrdiff_t row = 0; row < 100; ++row) {
            // sweeping the columns
            for (std::ptrdiff_t col = 0; col < 100; ++col) {
                // in c order, matching the dataset layout
                content[100 * row + col] = stamp(row, col);
            }
        }
        // deposit the whole product
        dataset.write(pyre::h5::datatype<cell_t>().id(), content.data());
    }

    // the read side: open the product back up, for reading only
    pyre::h5::File file { uri, H5F_ACC_RDONLY, {}, {} };
    // get the dataset
    auto dataset = file.openDataSet("product");
    // the memory datatype of the cells we are about to receive
    auto memtype = pyre::h5::datatype<cell_t>();

    // step 1: let the dataset describe itself
    // the description is pure arithmetic over shapes the dataset already knows: no matter
    // how large the product, nothing is allocated here
    auto tiling = dataset.tiling();

    // step 2: assemble the mosaic over the full description
    // a page holds a full chunk's worth of cells; measure one
    // NOTE: ergonomics: this bill of materials wants to be a one-line factory that takes
    // the tiling and hands back the mosaic
    paged_t::cell_count_type pageCells = 1;
    // as the volume of one tile
    for (auto extent : tiling.tileShape()) {
        // axis by axis
        pageCells *= extent;
    }
    // and there is one page per chunk
    paged_t::cell_count_type pages = 1;
    // as the volume of the tile grid
    for (auto extent : tiling.tiles()) {
        // axis by axis
        pages *= extent;
    }
    // the store: nothing resident, so the full product costs a page table and nothing more
    const paged_t store { pageCells, pages };
    // the mosaic: the product's own layout over the empty store
    const mosaic_t mosaic { tiling, store };

    // step 3: find the working set
    // the algorithm's window, in the product's own index space; it straddles chunk
    // boundaries and reaches into the clipped chunks at the edge of the product
    const pyre::h5::tiling_t::index_type base { 70, 70 };
    const pyre::h5::tiling_t::shape_type extent { 25, 25 };
    // the chunks the window touches: a 2x2 block of them, out of the twelve in the product
    auto touched = pyre::grid::tilesOverlapping(tiling, base, extent);

    // step 4: bring in the working set, chunk by chunk
    for (const auto & t : touched) {
        // the page that backs this chunk
        auto ordinal = tiling.tileOrdinal(t);
        // materialize it; this is the only allocation the read performs
        auto page = store.reside(ordinal);

        // the chunk's own layout, anchored where the chunk lives in the product; an edge
        // chunk keeps its full extent here, overhang included, matching its page exactly
        auto pane = tiling.tile(t);
        // but the file holds cells only inside the product, so clamp the chunk's box
        // against the extent, axis by axis; interior chunks pass through unclipped
        // room for the clamped corner and extent, and for the landing spot within the page
        pyre::h5::index_t fileOrigin(tiling.rank());
        pyre::h5::shape_t fileShape(tiling.rank());
        pyre::h5::index_t pageOrigin(tiling.rank());
        // go through the axes
        for (std::size_t axis = 0; axis < tiling.rank(); ++axis) {
            // the chunk begins at its anchor
            auto begin = pane.origin()[axis];
            // and would end a full chunk later, but never past the edge of the product
            auto end = std::min(begin + pane.shape()[axis], tiling.shape()[axis]);
            // the file block starts at the anchor
            // NOTE: ergonomics: the {pyre::grid} vocabulary is signed while the hdf5 one
            // is unsigned, so every crossing is a cast; the library should own this
            fileOrigin[axis] = static_cast<hsize_t>(begin);
            // and spans the clamped extent
            fileShape[axis] = static_cast<hsize_t>(end - begin);
            // the block lands at the head corner of the page
            pageOrigin[axis] = 0;
        }

        // describe the source: the clamped block of the product
        auto filespace = dataset.dataspace();
        // as a hyperslab selection
        filespace.slab(fileOrigin, fileShape);
        // describe the destination: the same block within a page-shaped extent, so that a
        // clipped chunk lands at the right offsets and the page padding is skipped
        // NOTE: ergonomics: this two-space dance is the heart of the read and wants to be
        // a single call: fill the pane of tile {t} from the dataset
        auto memspace =
            pyre::h5::DataSpace { pyre::h5::shape_t(pane.shape().begin(), pane.shape().end()) };
        // select the landing spot
        memspace.slab(pageOrigin, fileShape);
        // move the cells: the chunk flows from the file straight into its page
        dataset.read(memtype.id(), page, memspace.id(), filespace.id());
        // and record that the page now holds meaningful content
        store.validate(ordinal);
    }
    // the resident footprint is the working set, nothing more
    assert((store.residents() == touched.cells()));
    assert((store.bytes() == touched.cells() * pageCells * sizeof(cell_t)));

    // step 5: the algorithm reads the window through the mosaic, in the product's own
    // index space, with no idea that only four of the twelve chunks exist in memory
    for (auto row = base[0]; row < base[0] + extent[0]; ++row) {
        // sweeping the columns of the window
        for (auto col = base[1]; col < base[1] + extent[1]; ++col) {
            // every cell holds the stamp the producer wrote
            assert((mosaic[{ row, col }] == stamp(row, col)));
        }
    }
    // in particular the far corner, which lives in a chunk that is clipped along both axes
    assert((mosaic[{ 94, 94 }] == stamp(94, 94)));

    // clean up the scratch product
    std::remove(uri);

    // all done
    return 0;
}


// end of file
