// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//


namespace pyre::tensor {
    template <class T, class S>
    struct repacking_sum;

    template <int N, template <typename, int> class containerT>
    struct repacking_sum<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_sum<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_sum<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_sum<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_sum<
        pyre::grid::Diagonal<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_sum<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_sum<pyre::grid::Diagonal<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Diagonal<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_sum<
        pyre::grid::Diagonal<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_sum<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };

    template <class T, class S>
    struct repacking_prod;

    template <int N, template <typename, int> class containerT>
    struct repacking_prod<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_prod<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_prod<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_prod<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_prod<
        pyre::grid::Diagonal<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_prod<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_prod<
        pyre::grid::Diagonal<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Diagonal<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_prod<
        pyre::grid::Diagonal<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking_prod<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

} // namespace pyre::tensor


// end of file
