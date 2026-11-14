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


// a read through a memory type that names some of the members of a dataset reads just those
// members; every member it names is one the dataset has, so nothing is refused

// the layout of the stored samples
struct stored_t {
    // the first count
    std::uint16_t r;
    // and the second
    std::uint16_t i;
};


// read one member of a dataset of samples
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dataset_members_subset");

    // make the file
    pyre::h5::File file { "dataset_members_subset.h5", H5F_ACC_TRUNC, {}, {} };
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

    // a memory type that names the second member only
    auto second = pyre::h5::comptype_t(sizeof(std::uint16_t));
    second.insert("i", 0, pyre::h5::datatype<std::uint16_t>());
    // read it
    std::uint16_t read[3] = { 0, 0, 0 };
    dataset.read(second.id(), read);
    // and find the second count of each sample
    assert((read[0] == 2 && read[1] == 4 && read[2] == 6));

    // all done
    return 0;
}


// end of file
