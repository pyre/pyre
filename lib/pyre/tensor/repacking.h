// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// code guard
#pragma once


// my dependencies
#include "forward.h"


namespace pyre::tensor {

    // function to map the offset of a tensor {tensor1} with a given packing to the offset of
    // another tensor {tensor2} with a different packing
    template <int K, class tensor1, class tensor2>
    consteval auto map_offset()
        requires(tensor1::dims == tensor2::dims)
    {
        // get the index corresponding to the offset K in the packing of {tensor1}
        constexpr auto index = tensor1::layout().index(K);
        // return the offset corresponding to {index} in the packing of {tensor2}
        return tensor2::layout().offset(index);
    };

    template <class T, class S>
    struct repacking_sum;

    template <int N>
    struct repacking_sum<
        pyre::grid::Canonical<N>, pyre::grid::Canonical<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_sum<
        pyre::grid::Canonical<N>, pyre::grid::Symmetric<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_sum<
        pyre::grid::Symmetric<N>, pyre::grid::Canonical<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_sum<
        pyre::grid::Symmetric<N>, pyre::grid::Symmetric<N>> {
        using packing_type = pyre::grid::Symmetric<N>;
    };

    template <int N>
    struct repacking_sum<
        pyre::grid::Diagonal<N>, pyre::grid::Canonical<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_sum<
        pyre::grid::Canonical<N>, pyre::grid::Diagonal<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_sum<
        pyre::grid::Diagonal<N>, pyre::grid::Diagonal<N>> {
        using packing_type = pyre::grid::Diagonal<N>;
    };

    template <int N>
    struct repacking_sum<
        pyre::grid::Diagonal<N>, pyre::grid::Symmetric<N>> {
        using packing_type = pyre::grid::Symmetric<N>;
    };

    template <int N>
    struct repacking_sum<
        pyre::grid::Symmetric<N>, pyre::grid::Diagonal<N>> {
        using packing_type = pyre::grid::Symmetric<N>;
    };

    template <class T, class S>
    struct repacking_prod;

    template <int N>
    struct repacking_prod<
        pyre::grid::Canonical<N>, pyre::grid::Canonical<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_prod<
        pyre::grid::Canonical<N>, pyre::grid::Symmetric<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_prod<
        pyre::grid::Symmetric<N>, pyre::grid::Canonical<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_prod<
        pyre::grid::Symmetric<N>, pyre::grid::Symmetric<N>> {
        using packing_type = pyre::grid::Symmetric<N>;
    };

    template <int N>
    struct repacking_prod<
        pyre::grid::Diagonal<N>, pyre::grid::Canonical<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_prod<
        pyre::grid::Canonical<N>, pyre::grid::Diagonal<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_prod<
        pyre::grid::Diagonal<N>, pyre::grid::Diagonal<N>> {
        using packing_type = pyre::grid::Diagonal<N>;
    };

    template <int N>
    struct repacking_prod<
        pyre::grid::Diagonal<N>, pyre::grid::Symmetric<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

    template <int N>
    struct repacking_prod<
        pyre::grid::Symmetric<N>, pyre::grid::Diagonal<N>> {
        using packing_type = pyre::grid::Canonical<N>;
    };

} // namespace pyre::tensor


// end of file
