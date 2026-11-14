// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
#include <complex>
#include <cstddef>
// get the journal
#include <pyre/journal.h>
// get the h5 support
#include <pyre/h5.h>


// a dataset of complex numbers stored as a compound whose members are not named the way pyre
// names them reads as {std::complex}, its parts lined up with the members of the file by
// position

// the cell type
using cell_t = std::complex<float>;
// the layout of the stored values, with members named the way some producers name them
struct stored_t {
    // the real part
    float real;
    // and the imaginary part
    float imag;
};


// read complex numbers whose parts the file calls {real} and {imag}
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    // attribute whatever gets logged to this test
    pyre::journal::application("dataset_complex_members");

    // make the file
    pyre::h5::File file { "dataset_complex_members.h5", H5F_ACC_TRUNC, {}, {} };
    // describe the extent
    pyre::h5::DataSpace space { pyre::h5::shape_t { 3 } };
    // the stored layout
    auto stored = pyre::h5::comptype_t(sizeof(stored_t));
    stored.insert("real", offsetof(stored_t, real), pyre::h5::datatype<float>());
    stored.insert("imag", offsetof(stored_t, imag), pyre::h5::datatype<float>());
    // make the dataset
    auto dataset = file.createDataSet(
        "values", stored, space, pyre::h5::properties::DCPL(), pyre::h5::properties::DAPL());
    // and write three values into it
    const stored_t values[] = { { 1, 2 }, { 3, 4 }, { 5, 6 } };
    dataset.write(stored.id(), values);

    // the memory type for the cells takes the names of the members of the dataset, in order
    auto memtype = pyre::h5::types::Compound(H5Tcopy(dataset.memtype<cell_t>().id()));
    assert((memtype.members() == 2));
    assert((memtype.memberName(0) == "real"));
    assert((memtype.memberName(1) == "imag"));

    // read the values through it
    cell_t read[] = { { 0, 0 }, { 0, 0 }, { 0, 0 } };
    dataset.read(dataset.memtype<cell_t>().id(), read);
    // and find each part in its place
    assert((read[0] == cell_t { 1, 2 }));
    assert((read[1] == cell_t { 3, 4 }));
    assert((read[2] == cell_t { 5, 6 }));

    // all done
    return 0;
}


// end of file
