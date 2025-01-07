// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved
//


// code guard
#if !defined(pyre_tensor_traits_h)
#define pyre_tensor_traits_h


namespace pyre::tensor {

    // TOFIX: these functions should probably not be parked here...
    namespace {
        // helper function for expanding array in template parameter pack
        template <
            typename T, class packingT, auto arr,
            typename IS = decltype(std::make_index_sequence<arr.size()>())>
        struct tensor;

        // generator for a {tensor_t} from an array
        template <typename T, class packingT, auto arr, std::size_t... I>
        struct tensor<T, packingT, arr, std::index_sequence<I...>> {
            using type = tensor_t<T, packingT, arr[I]...>;
        };

        // method to extract the first {N} elements of an array into another array
        template <int N>
        constexpr auto first(const auto & array) -> std::array<int, N>
        {
            auto _first = [&array]<int... I>(integer_sequence<I...>) -> std::array<int, N> {
                return { array[I]... };
            };

            return _first(make_integer_sequence<N> {});
        }

        // method to extract the last {N} elements of an array into another array
        template <int N>
        constexpr auto last(const auto & array) -> std::array<int, N>
        {
            auto _last = [&array]<int... I>(integer_sequence<I...>) -> std::array<int, N> {
                return { array[I + array.size() - N]... };
            };

            return _last(make_integer_sequence<N> {});
        }

        // method to check the compatibility of the contracted indices
        // (i.e. the last N entries of {array1} and the first N entries of {array2} coincide)
        template <std::size_t N1, std::size_t N2>
        constexpr auto check(const std::array<int, N1> & array1, const std::array<int, N2> & array2)
            -> bool
        {
            // compute the rank of the contraction
            constexpr auto N = std::max(N1, N2) - std::min(N1, N2);

            auto _check = [&array1, &array2]<int... I>(integer_sequence<I...>) -> bool {
                return ((array2[I] == array1[I + array1.size() - N]) && ...);
            };

            return _check(make_integer_sequence<N> {});
        }
    } // namespace

    // the type resulting from the contraction of {T1} and {T2}
    template <class T1, class T2>
    struct contraction;

    // the tensor type resulting from the product of two arbitrary tensors {tensorT1} and {tensorT2}
    template <tensor_c tensorT1, tensor_c tensorT2>
        requires(check(tensorT1::dims, tensorT2::dims))
    struct contraction<tensorT1, tensorT2> {
    private:
        using T1 = typename tensorT1::scalar_type;
        using T2 = typename tensorT2::scalar_type;
        using scalar_type = typename std::invoke_result<std::multiplies<>, T1, T2>::type;
        static constexpr auto dims1 = tensorT1::dims;
        static constexpr auto dims2 = tensorT2::dims;
        static constexpr auto rank1 = dims1.size();
        static constexpr auto rank2 = dims2.size();
        static constexpr int rank = std::max(rank1, rank2) - std::min(rank1, rank2);
        static constexpr auto dims = (rank1 > rank2) ? first<rank>(dims1) : last<rank>(dims2);
        // using packingT1 = typename tensorT1::pack_t;
        // using packingT2 = typename tensorT2::pack_t;
        // using repacking_type = typename repacking_prod<packingT1, packingT2>::packing_type;
        using repacking_type =
            typename pyre::grid::Canonical<rank, int, std::array>; // TOFIX not general wrt packings

    public:
        using type = typename tensor<scalar_type, repacking_type, dims>::type;
    };

    // the type resulting from the product of {T1} and {T2}
    template <class T1, class T2>
    struct product;

    // the scalar type resulting from the dot product of two vectors {vectorT1} and {vectorT2}
    template <vector_c vectorT1, vector_c vectorT2>
    struct product<vectorT1, vectorT2> {
    private:
        using T1 = typename vectorT1::scalar_type;
        using T2 = typename vectorT2::scalar_type;

    public:
        using type = typename std::invoke_result<std::multiplies<>, T1, T2>::type;
    };

    // the vector type resulting from the row-column product of {matrixT} and {vectorT}
    template <matrix_c matrixT, vector_c vectorT>
    struct product<matrixT, vectorT> {
    private:
        using T1 = typename matrixT::scalar_type;
        using T2 = typename vectorT::scalar_type;
        using scalar_type = typename std::invoke_result<std::multiplies<>, T1, T2>::type;

    public:
        using type = vector_t<matrixT::dims[0], scalar_type>;
    };

    // the vector type resulting from the row-column product of {vectorT} and {matrixT}
    template <vector_c vectorT, matrix_c matrixT>
    struct product<vectorT, matrixT> {
    private:
        using T1 = typename vectorT::scalar_type;
        using T2 = typename matrixT::scalar_type;
        using scalar_type = typename std::invoke_result<std::multiplies<>, T1, T2>::type;

    public:
        using type = vector_t<matrixT::dims[1], scalar_type>;
    };

    // the matrix type resulting from the row-column product of {matrixT1} and {matrixT2}
    template <matrix_c matrixT1, matrix_c matrixT2>
    struct product<matrixT1, matrixT2> {
    private:
        using T1 = typename matrixT1::scalar_type;
        using T2 = typename matrixT2::scalar_type;
        using scalar_type = typename std::invoke_result<std::multiplies<>, T1, T2>::type;
        using packingT1 = typename matrixT1::pack_t;
        using packingT2 = typename matrixT2::pack_t;
        using repacking_type = typename repacking_prod<packingT1, packingT2>::packing_type;
        static constexpr int D1 = matrixT1::dims[0];
        static constexpr int D3 = matrixT2::dims[1];

    public:
        using type = matrix_t<D1, D3, scalar_type, repacking_type>;
    };

    // the type resulting from the product of {T1} and {T2}
    template <class T1, class T2>
    struct dyadic_product;

    // the vector type resulting from the dyadic product of {vectorT1} and {vectorT2}
    template <vector_c vectorT1, vector_c vectorT2>
    struct dyadic_product<vectorT1, vectorT2> {
    private:
        using T1 = typename vectorT1::scalar_type;
        using T2 = typename vectorT2::scalar_type;
        using scalar_type = typename std::invoke_result<std::multiplies<>, T1, T2>::type;

    public:
        using type = matrix_t<vectorT1::size, vectorT2::size, scalar_type>;
    };

    // the type resulting from the sum of {T1} and {T2}
    template <class T1, class T2>
    struct sum;

    // the tensor type resulting from the sum of two tensors
    template <typename T1, typename T2, class packingT1, class packingT2, int... I>
    struct sum<tensor_t<T1, packingT1, I...>, tensor_t<T2, packingT2, I...>> {
    private:
        using scalar_type = typename std::invoke_result<std::plus<>, T1, T2>::type;
        using repacking_type = typename repacking_sum<packingT1, packingT2>::packing_type;

    public:
        using type = tensor_t<scalar_type, repacking_type, I...>;
    };

} // namespace pyre::tensor


#endif

// end of file
