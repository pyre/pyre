// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the h5 support, which carries everything the recipe needs
#include <pyre/h5.h>


// the exhibit: the out-of-core read
//
// an algorithm wants a window of a large chunked product; the recipe reads only the chunks
// the window touches, lands each one in its own page with no intermediate copies, and hands
// the algorithm a mosaic it can address in the product's own index space
//
// the recipe, in four steps:
//   1. ask the dataset for a mosaic assembled over its own chunking; this is free: the
//      description is pure arithmetic, and nothing is resident
//   2. ask the mosaic which chunks the algorithm's window touches
//   3. {fill} each touched chunk, interleaving work with i/o at the per-tile seam
//   4. the algorithm reads the window through the mosaic, unaware it is out-of-core
// and a coda for algorithms that cannot work on partial results: declare the smallest
// mosaic that covers the window, and {fill} all of it in one call

// the cell type of the product; this is the one thing the recipe fixes at compile time,
// since the code that receives the data must name the type in order to allocate for it
using cell_t = double;

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
        // the producer writes through a mosaic of its own: the mirror of the recipe below
        auto product = dataset.mosaic<cell_t>();
        // its tiled layout
        const auto & tiles = product.packing();
        // deposit chunk by chunk
        for (const auto & t : product.tilesOverlapping(tiles.origin(), tiles.shape())) {
            // the page that backs this chunk
            auto ordinal = tiles.tileOrdinal(t);
            // materialize it
            product.storage().reside(ordinal);
            // and deposit through the pane, whose indices are product coordinates
            auto pane = product.pane(t);
            // fill every cell, padding included; only cells inside the product persist
            for (const auto & idx : pane.packing()) {
                // with a value that encodes its own coordinates
                pane[idx] = stamp(idx[0], idx[1]);
            }
            // declare the deposit
            product.storage().validate(ordinal);
            // and its divergence from the file
            product.storage().taint(ordinal);
        }
        // make the file agree
        dataset.flush(product);
    }

    // the read side: open the product back up, for reading only
    pyre::h5::File file { uri, H5F_ACC_RDONLY, {}, {} };
    // get the dataset
    auto dataset = file.openDataSet("product");

    // step 1: ask the dataset for a mosaic assembled over its own chunking
    // no matter how large the product, this costs a page table and nothing more: the
    // layout is pure arithmetic, and no page is resident until a chunk is touched
    const auto mosaic = dataset.mosaic<cell_t>();

    // step 2: find the working set
    // the algorithm's window, in the product's own index space; it straddles chunk
    // boundaries and reaches into the clipped chunks at the edge of the product
    const pyre::h5::tiling_t::index_type base { 70, 70 };
    const pyre::h5::tiling_t::shape_type extent { 25, 25 };
    // the chunks the window touches: a 2x2 block of them, out of the twelve in the product
    auto touched = mosaic.tilesOverlapping(base, extent);

    // step 3: bring in the working set, chunk by chunk
    // the per-tile call is the seam for algorithms that can process partial results: work
    // interleaves with i/o, one chunk at a time
    for (const auto & t : touched) {
        // pull the chunk into its page: {fill} materializes the page, clamps the chunk
        // against the edge of the product, lands the cells, and records the deposit
        dataset.fill(mosaic, t);
    }
    // the resident footprint is the working set, nothing more
    assert((mosaic.storage().residents() == touched.cells()));
    assert(
        (mosaic.storage().bytes()
         == touched.cells() * mosaic.storage().pageCells() * sizeof(cell_t)));

    // step 4: the algorithm reads the window through the mosaic, in the product's own
    // index space, with no idea that only four of the twelve chunks exist in memory
    // the window is itself a layout: a canonical box of the given {extent} anchored at
    // {base}, and iterating a layout generates every index in its box
    for (const auto & idx : pyre::h5::packing_t { extent, base }) {
        // every cell holds the stamp the producer wrote
        assert((mosaic[idx] == stamp(idx[0], idx[1])));
    }
    // in particular the far corner, which lives in a chunk that is clipped along both axes
    assert((mosaic[{ 94, 94 }] == stamp(94, 94)));

    // the coda: an algorithm that cannot work on partial results declares the smallest
    // mosaic that covers its window and asks for all of it; no loop, no ceremony
    auto window = dataset.mosaic<cell_t>(base, extent);
    // make the whole window resident
    dataset.fill(window);
    // the window mosaic holds exactly the touched chunks
    assert((window.storage().residents() == touched.cells()));
    // and addresses the product in its own index space: the near corner of the window
    assert((window[{ 70, 70 }] == stamp(70, 70)));
    // and the far one, out in the doubly clipped chunk
    assert((window[{ 94, 94 }] == stamp(94, 94)));


    // all done
    return 0;
}


// end of file
