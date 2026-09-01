// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the h5 support
#include <pyre/h5.h>


// the block the tile lands in
using heap_t = pyre::memory::heap_t<double>;


// verify that a tile can be read and written visiting only every n-th cell along each axis:
// the decimated view a zoomed out reader wants, assembled without moving the cells it skips
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dataset_strided");

    // the scratch product
    auto uri = "dataset_strided.h5";
    // a scope, so the file closes before the cleanup
    {
        // make it
        pyre::h5::File file { uri, H5F_ACC_TRUNC, {}, {} };

        // a small raster, whose cells will each be made to say where they live so that a
        // sample can be checked against the coordinate it claims to have come from
        auto extent = pyre::h5::shape_t { 32, 32 };
        pyre::h5::DataSpace space { extent };
        // the cell type the whole exhibit trades in
        auto cell = pyre::h5::datatype<double>();
        // a dataset to read back from, and one to scatter into
        auto src = file.createDataSet(
            "src", cell, space, pyre::h5::properties::DCPL(), pyre::h5::properties::DAPL());
        auto dst = file.createDataSet(
            "dst", cell, space, pyre::h5::properties::DCPL(), pyre::h5::properties::DAPL());

        // room for the whole raster; the block counts its cells with a signed type, so
        // carry the product across the signedness boundary rather than narrow it silently
        heap_t whole { static_cast<heap_t::cell_count_type>(extent[0] * extent[1]) };
        // give every cell its own row and column, encoded so either can be recovered
        for (std::size_t row = 0; row < extent[0]; ++row) {
            for (std::size_t col = 0; col < extent[1]; ++col) {
                // stamp the coordinate into the cell
                whole[row * extent[1] + col] = static_cast<double>(100 * row + col);
            }
        }
        // lay the raster down the ordinary way
        pyre::h5::write(src, whole, cell, pyre::h5::shape_t { 0, 0 }, extent);

        // now pull a decimated view: every second row and every fourth column, which is the
        // case that catches an implementation assuming one stride for the whole request
        auto stride = pyre::h5::shape_t { 2, 4 };
        auto shape = pyre::h5::shape_t { 8, 4 };
        auto origin = pyre::h5::shape_t { 1, 3 };
        // the samples arrive packed, so the destination holds only as many as come back
        heap_t sampled { static_cast<heap_t::cell_count_type>(shape[0] * shape[1]) };
        // take them
        pyre::h5::read(src, sampled, cell, origin, shape, stride);

        // every sample has to be the cell a caller would have reached for by hand
        for (std::size_t row = 0; row < shape[0]; ++row) {
            for (std::size_t col = 0; col < shape[1]; ++col) {
                // the cell it was drawn from, walking out from the origin by the stride
                auto sourceRow = origin[0] + row * stride[0];
                auto sourceCol = origin[1] + col * stride[1];
                // and the value that cell was given when the raster was laid down
                auto expected = static_cast<double>(100 * sourceRow + sourceCol);
                // which is what should have arrived
                assert((sampled[row * shape[1] + col] == expected));
            }
        }

        // the write side scatters: put those samples into the other dataset at the same
        // spacing they were drawn from
        pyre::h5::write(dst, sampled, cell, origin, shape, stride);

        // read them back one cell at a time, to confirm they landed where they were aimed
        // rather than packed into a block at the corner
        heap_t one { 1 };
        // go through the samples
        for (std::size_t row = 0; row < shape[0]; ++row) {
            for (std::size_t col = 0; col < shape[1]; ++col) {
                // the slot this sample should have landed in
                auto targetRow = origin[0] + row * stride[0];
                auto targetCol = origin[1] + col * stride[1];
                // read that single cell
                pyre::h5::read(
                    dst, one, cell, pyre::h5::shape_t { targetRow, targetCol },
                    pyre::h5::shape_t { 1, 1 });
                // and it has to carry the value that travelled with it
                assert((one[0] == static_cast<double>(100 * targetRow + targetCol)));
            }
        }
    }

    // all done
    return 0;
}


// end of file
