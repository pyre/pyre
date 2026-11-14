// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
#include <cstddef>
#include <cstdint>
// get the journal
#include <pyre/journal.h>
// get the grids
#include <pyre/grid.h>
// get the h5 support
#include <pyre/h5.h>


// a strided tile read into a grid whose memory type is deduced from its cells: the read lines
// the cells up with the members of the dataset by position, so radar samples stored under the
// names NISAR uses come back with each count in its place

// the cell type
using cell_t = pyre::memory::iq_t<std::uint16_t>;
// the grid the tile lands in
using grid_t = pyre::grid::grid_t<pyre::grid::canonical_t<2>, pyre::memory::heap_t<cell_t>>;
// the layout of the stored samples
struct stored_t {
    // the first count
    std::uint16_t r;
    // and the second
    std::uint16_t i;
};


// read every other sample of a dataset of radar samples
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dataset_read_deduced");

    // the extent of the dataset
    const int side = 4;
    // make the file
    pyre::h5::File file { "dataset_read_deduced.h5", H5F_ACC_TRUNC, {}, {} };
    // describe the extent
    pyre::h5::DataSpace space { pyre::h5::shape_t { side, side } };
    // the stored layout
    auto stored = pyre::h5::comptype_t(sizeof(stored_t));
    stored.insert("r", offsetof(stored_t, r), pyre::h5::datatype<std::uint16_t>());
    stored.insert("i", offsetof(stored_t, i), pyre::h5::datatype<std::uint16_t>());
    // make the dataset
    auto dataset = file.createDataSet(
        "samples", stored, space, pyre::h5::properties::DCPL(), pyre::h5::properties::DAPL());
    // fill it with samples whose counts say where they are
    stored_t samples[side * side];
    for (int line = 0; line < side; ++line) {
        for (int sample = 0; sample < side; ++sample) {
            // the first count names the line and the sample, the second its complement
            auto code = static_cast<std::uint16_t>(10 * line + sample);
            samples[line * side + sample] =
                stored_t { code, static_cast<std::uint16_t>(100 - code) };
        }
    }
    // and write them
    dataset.write(stored.id(), samples);

    // read every other sample along each axis, starting at the corner
    auto tile = pyre::h5::read<grid_t>(dataset, { 0, 0 }, { 2, 2 }, { 2, 2 });
    // every cell holds the counts of the sample it was drawn from, each in its place
    for (int line = 0; line < 2; ++line) {
        for (int sample = 0; sample < 2; ++sample) {
            // the code of the sample at twice the position
            auto code = static_cast<std::uint16_t>(10 * 2 * line + 2 * sample);
            // check
            assert((
                tile[{ line, sample }] == cell_t { code, static_cast<std::uint16_t>(100 - code) }));
        }
    }

    // all done
    return 0;
}


// end of file
