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


// a read through a memory type that names a member the dataset does not have is refused, and
// leaves its buffer alone; hdf5 matches compound members by name, so without the refusal it
// would fill only the members the two types share and report success

// the cell type, whose members are named {i} and {q}
using cell_t = pyre::memory::iq_t<std::uint16_t>;
// the layout of the stored samples, whose members are named {r} and {i}
struct stored_t {
    // the first count
    std::uint16_t r;
    // and the second
    std::uint16_t i;
};


// read samples through a memory type whose member names do not match the dataset's
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dataset_members_read");

    // the refusal is expected: keep it from ending the test, and send it to the trash
    auto firewall = pyre::journal::firewall_t("pyre.h5.dataset");
    firewall.fatal(false);
    firewall.device<pyre::journal::trash_t>();

    // make the file
    pyre::h5::File file { "dataset_members_read.h5", H5F_ACC_TRUNC, {}, {} };
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

    // a buffer whose cells hold a value the dataset does not
    cell_t buffer[] = { { 7, 7 }, { 7, 7 }, { 7, 7 } };
    // read through the memory type of the cells, whose {q} the dataset does not have
    dataset.read(pyre::h5::datatype<cell_t>().id(), buffer);
    // the read was refused, so every cell is as it was
    for (const auto & cell : buffer) {
        assert((cell == cell_t { 7, 7 }));
    }

    // all done
    return 0;
}


// end of file
