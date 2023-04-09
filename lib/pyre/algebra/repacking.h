// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//


namespace pyre::algebra {
    template <class T, class S>
    struct repacking;

    template <int N, template <typename, int> class containerT>
    struct repacking<pyre::grid::Canonical<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking<pyre::grid::Canonical<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking<pyre::grid::Symmetric<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking<pyre::grid::Symmetric<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking<pyre::grid::Diagonal<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking<pyre::grid::Canonical<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking<pyre::grid::Diagonal<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Diagonal<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking<pyre::grid::Diagonal<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };

    template <int N, template <typename, int> class containerT>
    struct repacking<pyre::grid::Symmetric<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };
}


// end of file
