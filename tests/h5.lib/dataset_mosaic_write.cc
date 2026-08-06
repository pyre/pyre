// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// for the poison reference pattern
#include <cstring>
// get the h5 support, which carries everything the recipe needs
#include <pyre/h5.h>


// the exhibit: the out-of-core write
//
// a producer assembles a mosaic over the dataset it is filling, deposits content through
// panes — declaring as it goes — and pushes the divergence back into the file; the exhibit
// then updates the product in place, and closes with the uninitialized-cell caveat and the
// {poison} aid
//
// the recipe:
//   1. create the product and ask it for a mosaic, exactly as a reader would
//   2. deposit chunk by chunk: materialize the page, write through the pane, declare the
//      deposit ({validate}) and its divergence from the file ({taint})
//   3. {flush} pushes what diverged; pages never touched, or already saved, are skipped

// the cell type of the product
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
    pyre::journal::application("dataset_mosaic_write");

    // the scratch product
    auto uri = "dataset_mosaic_write.h5";
    // make the file
    pyre::h5::File file { uri, H5F_ACC_TRUNC, {}, {} };
    // describe the extent
    pyre::h5::DataSpace space { pyre::h5::shape_t { 100, 100 } };
    // and the chunking, deliberately not a divisor of the extent along either axis
    pyre::h5::properties::DCPL dcpl;
    dcpl.chunk(pyre::h5::shape_t { 30, 40 });
    // make the dataset
    auto dataset = file.createDataSet(
        "product", pyre::h5::datatype<cell_t>(), space, dcpl, pyre::h5::properties::DAPL());

    // act one: produce the whole product through a mosaic
    {
        // the producer's mosaic, over the dataset's own chunking
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
        // make the file agree: all twelve chunks push, clamped against the extent
        dataset.flush(product);
        // and the pushed pages are marked clean, so a second flush moves nothing
        dataset.flush(product);
    }

    // act two: verify through the read side
    {
        // a fresh mosaic
        auto verify = dataset.mosaic<cell_t>();
        // make it all resident
        dataset.fill(verify);
        // and sweep the whole product
        for (const auto & idx : pyre::h5::packing_t { { 100, 100 } }) {
            // every cell holds what the producer deposited
            assert((verify[idx] == stamp(idx[0], idx[1])));
        }
    }

    // act three: update the product in place, touching only one chunk
    {
        // the cell to change, and the value to change it to
        const pyre::h5::tiling_t::index_type probe { 35, 45 };
        // read-modify-write: a fresh mosaic, one chunk pulled
        auto mosaic = dataset.mosaic<cell_t>();
        // the chunk that holds the probe
        auto t = mosaic.packing().tileOf(probe);
        // pull it
        dataset.fill(mosaic, t);
        // change the cell through the mosaic, in product coordinates
        mosaic[probe] = 999.0;
        // declare the divergence; assignment through a c++ reference is invisible to the store
        mosaic.storage().taint(mosaic.packing().tileOrdinal(t));
        // the wholesale flush pushes just this chunk: nothing else is resident
        dataset.flush(mosaic);

        // pull the neighborhood back and check
        auto check = dataset.mosaic<cell_t>();
        // the chunk in question
        dataset.fill(check, t);
        // the probe changed
        assert((check[probe] == 999.0));
        // its neighbor did not
        assert((check[{ 35, 46 }] == stamp(35, 46)));
    }

    // act four: the uninitialized-cell caveat, and the {poison} aid
    {
        // a mosaic for a partial deposit into the first chunk
        auto partial = dataset.mosaic<cell_t>();
        // the chunk at the origin
        const pyre::h5::tiling_t::index_type t { 0, 0 };
        // the page that backs it
        auto ordinal = partial.packing().tileOrdinal(t);
        // materialize it with a recognizable pattern, so unwritten cells stand out
        partial.storage().poison(ordinal);
        // deposit a single cell through the pane
        auto pane = partial.pane(t);
        pane[{ 0, 0 }] = 7.0;
        // declare
        partial.storage().validate(ordinal);
        partial.storage().taint(ordinal);
        // push just this chunk; the unwritten cells carry the pattern into the file
        dataset.flush(partial, t);

        // read the chunk back
        auto check = dataset.mosaic<cell_t>();
        dataset.fill(check, t);
        // the written cell holds its value
        assert((check[{ 0, 0 }] == 7.0));
        // and an unwritten one holds the pattern, bit for bit: caveat emptor, made visible
        cell_t pattern;
        std::memset(&pattern, 0xdb, sizeof(pattern));
        auto cell = check[{ 5, 5 }];
        assert((std::memcmp(&cell, &pattern, sizeof(pattern)) == 0));
    }


    // all done
    return 0;
}


// end of file
