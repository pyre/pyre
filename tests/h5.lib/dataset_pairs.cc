// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
// get the h5 support
#include <pyre/h5.h>


// a dataset of radar samples stored the way NISAR stores them, as a compound of two counts named
// {r} and {i}, reads and writes through pyre as {iq_t}, its counts lined up with the members of
// the file by position; hdf5 matches compound members by name, so a memory type that used the
// names of the fields of {iq_t} would put the file's second count in {i} and leave {q} alone

// the cell type
using cell_t = pyre::memory::iq_t<std::uint16_t>;
// the layout of the stored samples, independent of the cell type
struct stored_t {
    // the first count
    std::uint16_t r;
    // and the second
    std::uint16_t i;
};


// exercise reading and writing samples whose stored members are not named after the cell
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dataset_pairs");

    // the scratch product
    auto uri = "dataset_pairs.h5";
    // make the file
    pyre::h5::File file { uri, H5F_ACC_TRUNC, {}, {} };
    // describe the extent
    pyre::h5::DataSpace space { pyre::h5::shape_t { 3 } };
    // the stored layout: two counts named the way the files of the mission name them
    auto stored = pyre::h5::comptype_t(sizeof(stored_t));
    stored.insert("r", offsetof(stored_t, r), pyre::h5::datatype<std::uint16_t>());
    stored.insert("i", offsetof(stored_t, i), pyre::h5::datatype<std::uint16_t>());
    // make the dataset
    auto dataset = file.createDataSet(
        "samples", stored, space, pyre::h5::properties::DCPL(), pyre::h5::properties::DAPL());
    // and write three samples into it, each count with its own value
    const stored_t samples[] = { { 1, 2 }, { 3, 4 }, { 5, 6 } };
    dataset.write(stored.id(), samples);

    // the memory type for the cells takes the names of the members of the dataset, in order
    auto memtype = pyre::h5::types::Compound(H5Tcopy(dataset.memtype<cell_t>().id()));
    assert((memtype.members() == 2));
    assert((memtype.memberName(0) == "r"));
    assert((memtype.memberName(1) == "i"));
    // and places them where the fields of the cell sit
    assert((memtype.memberOffset(0) == offsetof(cell_t, i)));
    assert((memtype.memberOffset(1) == offsetof(cell_t, q)));

    // a mosaic of samples over the dataset
    auto mosaic = dataset.mosaic<cell_t>();
    // pull its cells in
    dataset.fill(mosaic);
    // every sample reads back with its counts in place
    auto pane = mosaic.pane(mosaic.packing().origin());
    assert((pane[0] == cell_t { 1, 2 }));
    assert((pane[1] == cell_t { 3, 4 }));
    assert((pane[2] == cell_t { 5, 6 }));

    // change one sample through the mosaic
    pane[1] = cell_t { 30, 40 };
    // mark its page as diverged from the file
    mosaic.storage().taint(0);
    // and push it back
    dataset.flush(mosaic);
    // read the stored layout straight out of the file
    stored_t read[3];
    dataset.read(stored.id(), read);
    // the counts landed in their own members
    assert((read[1].r == 30 && read[1].i == 40));
    // and the rest are untouched
    assert((read[0].r == 1 && read[0].i == 2));
    assert((read[2].r == 5 && read[2].i == 6));

    // all done
    return 0;
}


// end of file
