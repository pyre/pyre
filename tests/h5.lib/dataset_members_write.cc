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
// get the h5 support
#include <pyre/h5.h>


// a write through a memory type that names a member the dataset does not have is refused, and
// leaves the dataset alone; hdf5 matches compound members by name, so without the refusal it
// would store only the members the two types share and report success

// the cell type, whose members are named {i} and {q}
using cell_t = pyre::memory::iq_t<std::uint16_t>;
// the layout of the stored samples, whose members are named {r} and {i}
struct stored_t {
    // the first count
    std::uint16_t r;
    // and the second
    std::uint16_t i;
};


// write samples through a memory type whose member names do not match the dataset's
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dataset_members_write");

    // the refusal is expected: keep it from ending the test, and send it to the trash
    auto firewall = pyre::journal::firewall_t("pyre.h5.dataset");
    firewall.fatal(false);
    firewall.device<pyre::journal::trash_t>();

    // make the file
    pyre::h5::File file { "dataset_members_write.h5", H5F_ACC_TRUNC, {}, {} };
    // describe the extent
    pyre::h5::DataSpace space { pyre::h5::shape_t { 3 } };
    // the stored layout
    auto stored = pyre::h5::comptype_t(sizeof(stored_t));
    stored.insert("r", offsetof(stored_t, r), pyre::h5::datatype<std::uint16_t>());
    stored.insert("i", offsetof(stored_t, i), pyre::h5::datatype<std::uint16_t>());
    // make the dataset
    auto dataset = file.createDataSet(
        "samples", stored, space, pyre::h5::properties::DCPL(), pyre::h5::properties::DAPL());
    // and write three samples into it
    const stored_t samples[] = { { 1, 2 }, { 3, 4 }, { 5, 6 } };
    dataset.write(stored.id(), samples);

    // other samples
    const cell_t replacements[] = { { 10, 20 }, { 30, 40 }, { 50, 60 } };
    // written through the memory type of the cells, whose {q} the dataset does not have
    dataset.write(pyre::h5::datatype<cell_t>().id(), replacements);

    // read the stored layout straight out of the file
    stored_t read[3];
    dataset.read(stored.id(), read);
    // the write was refused, so every sample is as it was
    assert((read[0].r == 1 && read[0].i == 2));
    assert((read[1].r == 3 && read[1].i == 4));
    assert((read[2].r == 5 && read[2].i == 6));

    // all done
    return 0;
}


// end of file
