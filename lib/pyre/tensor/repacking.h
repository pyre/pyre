// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//


namespace pyre::tensor {
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
