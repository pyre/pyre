// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Float.h"
// the reporting of library refusals
#include "../diagnostics.h"
// the predefined type i can copy
#include "Predefined.h"


// adopt an existing raw handle
pyre::h5::types::Float::Float(id_type id) : Atom(id) {}


// make an independent copy of a predefined float type
pyre::h5::types::Float::Float(const Predefined & type) :
    Atom(static_cast<id_type>(H5Tcopy(type.id())))
{
    // if the library refused
    if (!valid()) {
        // complain
        complain("pyre.h5.types", "copying a predefined float type");
    }
}


// my exponent bias
auto
pyre::h5::types::Float::bias() const -> std::size_t
{
    // ask the library
    auto answer = H5Tget_ebias(id());
    // if it refused
    if (answer == 0) {
        // complain
        complain("pyre.h5.types", "retrieving the exponent bias of a float type");
        // and hand back nothing
        return 0;
    }
    // otherwise, report
    return answer;
}


// set my exponent bias
auto
pyre::h5::types::Float::setBias(std::size_t bias) -> void
{
    // hand it to the library
    if (H5Tset_ebias(id(), bias) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the exponent bias of a float type");
    }
    // all done
    return;
}


// my mantissa normalization strategy
auto
pyre::h5::types::Float::normalization() const -> norm_type
{
    // ask the library
    auto answer = H5Tget_norm(id());
    // if it refused
    if (answer == H5T_NORM_ERROR) {
        // complain
        complain("pyre.h5.types", "retrieving the mantissa normalization of a float type");
        // and hand back nothing
        return H5T_NORM_ERROR;
    }
    // otherwise, report
    return answer;
}


// set my mantissa normalization strategy
auto
pyre::h5::types::Float::setNorm(norm_type norm) -> void
{
    // hand it to the library
    if (H5Tset_norm(id(), norm) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the mantissa normalization of a float type");
    }
    // all done
    return;
}


// my internal padding strategy
auto
pyre::h5::types::Float::inpad() const -> pad_type
{
    // ask the library
    auto answer = H5Tget_inpad(id());
    // if it refused
    if (answer == H5T_PAD_ERROR) {
        // complain
        complain("pyre.h5.types", "retrieving the internal padding of a float type");
        // and hand back nothing
        return H5T_PAD_ERROR;
    }
    // otherwise, report
    return answer;
}


// set my internal padding strategy
auto
pyre::h5::types::Float::setInpad(pad_type pad) -> void
{
    // hand it to the library
    if (H5Tset_inpad(id(), pad) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the internal padding of a float type");
    }
    // all done
    return;
}


// my bit layout
auto
pyre::h5::types::Float::fields() const -> fields_type
{
    // make room for the answer
    std::size_t spos, epos, esize, mpos, msize;
    // ask the library; an answer it refuses to give is not one to read
    if (H5Tget_fields(id(), &spos, &epos, &esize, &mpos, &msize) < 0) {
        // so complain
        complain("pyre.h5.types", "retrieving the bit layout of a float type");
        // and hand back an empty layout
        return { 0, 0, 0, 0, 0 };
    }
    // pack and ship
    return { spos, epos, esize, mpos, msize };
}


// set my bit layout
auto
pyre::h5::types::Float::setFields(
    std::size_t spos, std::size_t epos, std::size_t esize, std::size_t mpos, std::size_t msize)
    -> void
{
    // hand them to the library
    if (H5Tset_fields(id(), spos, epos, esize, mpos, msize) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the bit layout of a float type");
    }
    // all done
    return;
}


// end of file
