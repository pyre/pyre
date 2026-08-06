// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the h5 support
#include <pyre/h5.h>


// verify that a chunked dataset describes itself in the {pyre::grid} vocabulary: its extent
// as a canonical layout, and its chunking as the tiled layout a mosaic is assembled over
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dataset_tiling");

    // the scratch product
    auto uri = "dataset_tiling.h5";
    // a scope, so the file closes before the cleanup
    {
        // make it
        pyre::h5::File file { uri, H5F_ACC_TRUNC, {}, {} };

        // describe a product diced into chunks that do not divide its extent evenly, so the
        // edge padding is in play
        pyre::h5::DataSpace space { pyre::h5::shape_t { 100, 100 } };
        // creation properties that dice it
        pyre::h5::properties::DCPL dcpl;
        // into rectangular chunks
        dcpl.chunk(pyre::h5::shape_t { 30, 40 });
        // make the dataset
        auto dataset = file.createDataSet(
            "product", pyre::h5::datatype<double>(), space, dcpl, pyre::h5::properties::DAPL());

        // the extent crosses over as a canonical layout
        auto packing = dataset.packing();
        // with the shape of the product
        assert((packing.shape() == pyre::h5::packing_t::shape_type { 100, 100 }));
        // and one cell per element
        assert((packing.cells() == 100 * 100));
        // the dataspace agrees with itself across the wrapper boundary
        assert((dataset.dataspace().sameExtent(space)));

        // the chunking crosses over as a tiled layout
        auto tiling = dataset.tiling();
        // whose box is the product
        assert((tiling.shape() == pyre::h5::tiling_t::shape_type { 100, 100 }));
        // whose tile is the chunk
        assert((tiling.tileShape() == pyre::h5::tiling_t::shape_type { 30, 40 }));
        // covered by enough chunks along each axis, edges rounded up
        assert((tiling.tiles() == pyre::h5::tiling_t::shape_type { 4, 3 }));
        // with the edge overhang stored as padding, exactly the way hdf5 stores the product
        assert((tiling.cells() == (4 * 30) * (3 * 40)));

        // the working set machinery composes: an algorithm's window, not aligned with the
        // chunks, touches a computable set of them
        auto touched = pyre::grid::tilesOverlapping(
            tiling, pyre::h5::tiling_t::index_type { 25, 35 },
            pyre::h5::tiling_t::shape_type { 20, 20 });
        // the window leans into the chunk at the origin
        assert((touched.origin() == pyre::h5::tiling_t::index_type { 0, 0 }));
        // and spills over into a 2x2 block of them
        assert((touched.shape() == pyre::h5::tiling_t::shape_type { 2, 2 }));

        // a dataset that is not chunked is a single slab
        auto flat = file.createDataSet(
            "flat", pyre::h5::datatype<double>(),
            pyre::h5::DataSpace { pyre::h5::shape_t { 8, 5 } }, pyre::h5::properties::DCPL(),
            pyre::h5::properties::DAPL());
        // its tiling is total: one tile that covers the whole box
        auto slab = flat.tiling();
        // the box is the extent
        assert((slab.shape() == pyre::h5::tiling_t::shape_type { 8, 5 }));
        // the tile is the box
        assert((slab.tileShape() == pyre::h5::tiling_t::shape_type { 8, 5 }));
        // and there is exactly one of them
        assert((slab.tiles() == pyre::h5::tiling_t::shape_type { 1, 1 }));
    }

    // all done
    return 0;
}


// end of file
