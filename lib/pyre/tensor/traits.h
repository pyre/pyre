// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved
//


// code guard
#if !defined(pyre_tensor_traits_h)
#define pyre_tensor_traits_h


namespace pyre::tensor {

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
