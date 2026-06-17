// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
#include "external.h"

namespace pyre::gsl::py {

void
permutation(::py::module & m)
{
    // register the Permutation type
    ::py::class_<pyre::gsl::Permutation>(m, "Permutation");

    // allocate a new permutation of size n
    m.def(
        "permutation_alloc",
        [](size_t n) {
            return std::make_unique<pyre::gsl::Permutation>(n);
        },
        "n"_a,
        "allocate a permutation of the given size");

    // initialize a permutation to the identity
    m.def(
        "permutation_init",
        [](pyre::gsl::Permutation & p) {
            gsl_permutation_init(p.ptr);
        },
        "p"_a,
        "initialize a permutation to the identity");

    // copy src into dst
    m.def(
        "permutation_copy",
        [](pyre::gsl::Permutation & dst, pyre::gsl::Permutation & src) {
            gsl_permutation_memcpy(dst.ptr, src.ptr);
        },
        "dst"_a, "src"_a,
        "copy one permutation into another");

    // get element at index
    m.def(
        "permutation_get",
        [](pyre::gsl::Permutation & p, size_t index) -> size_t {
            return gsl_permutation_get(p.ptr, index);
        },
        "p"_a, "index"_a,
        "get the value of a permutation element");

    // swap two elements
    m.def(
        "permutation_swap",
        [](pyre::gsl::Permutation & p, size_t i, size_t j) {
            gsl_permutation_swap(p.ptr, i, j);
        },
        "p"_a, "i"_a, "j"_a,
        "swap two elements of a permutation");

    // return the size
    m.def(
        "permutation_size",
        [](pyre::gsl::Permutation & p) -> size_t {
            return gsl_permutation_size(p.ptr);
        },
        "p"_a,
        "return the size of a permutation");

    // check validity
    m.def(
        "permutation_valid",
        [](pyre::gsl::Permutation & p) -> bool {
            return gsl_permutation_valid(p.ptr) == GSL_SUCCESS;
        },
        "p"_a,
        "check whether the permutation is valid");

    // reverse in place
    m.def(
        "permutation_reverse",
        [](pyre::gsl::Permutation & p) {
            gsl_permutation_reverse(p.ptr);
        },
        "p"_a,
        "reverse a permutation in place");

    // compute and return the inverse as a new Permutation
    m.def(
        "permutation_inverse",
        [](pyre::gsl::Permutation & p) {
            gsl_permutation * inv = gsl_permutation_alloc(gsl_permutation_size(p.ptr));
            gsl_permutation_inverse(inv, p.ptr);
            return std::make_unique<pyre::gsl::Permutation>(inv, true);
        },
        "p"_a,
        "return the inverse of a permutation as a new permutation");

    // advance to the next permutation in lexicographic order
    m.def(
        "permutation_next",
        [](pyre::gsl::Permutation & p) -> bool {
            return gsl_permutation_next(p.ptr) == GSL_SUCCESS;
        },
        "p"_a,
        "advance to the next permutation; return True if successful");

    // step back to the previous permutation in lexicographic order
    m.def(
        "permutation_prev",
        [](pyre::gsl::Permutation & p) -> bool {
            return gsl_permutation_prev(p.ptr) == GSL_SUCCESS;
        },
        "p"_a,
        "step back to the previous permutation; return True if successful");
}

} // namespace pyre::gsl::py

// end of file
