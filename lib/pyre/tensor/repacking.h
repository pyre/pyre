// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved
//


// code guard
#if !defined(pyre_tensor_repacking_h)
#define pyre_tensor_repacking_h


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

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_sum<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_sum<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_sum<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_sum<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_sum<
        pyre::grid::Diagonal<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_sum<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_sum<pyre::grid::Diagonal<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Diagonal<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_sum<
        pyre::grid::Diagonal<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_sum<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };

    template <class T, class S>
    struct repacking_prod;

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_prod<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_prod<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_prod<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_prod<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Symmetric<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_prod<
        pyre::grid::Diagonal<N, containerT>, pyre::grid::Canonical<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_prod<
        pyre::grid::Canonical<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_prod<
        pyre::grid::Diagonal<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Diagonal<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_prod<
        pyre::grid::Diagonal<N, containerT>, pyre::grid::Symmetric<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

    template <int N, template <typename, std::size_t> class containerT>
    struct repacking_prod<
        pyre::grid::Symmetric<N, containerT>, pyre::grid::Diagonal<N, containerT>> {
        using packing_type = pyre::grid::Canonical<N, containerT>;
    };

} // namespace pyre::tensor


#endif

// end of file
