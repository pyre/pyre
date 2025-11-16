// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved


// code guard
#if !defined(pyre_tensor_api_h)
#define pyre_tensor_api_h


namespace pyre::tensor {
    // typedef for real values
    using real = double;

    // type alias for canonical packing
    template <int D>
    using canonical_packing_t = pyre::grid::canonical_t<D, int>;

    // type alias for diagonal packing
    template <int D>
    using diagonal_packing_t = pyre::grid::diagonal_t<D, int>;

    // type alias for symmetric packing
    template <int D>
    using symmetric_packing_t = pyre::grid::symmetric_t<D, int>;

    // typedef for vectors
    template <int D, typename T = real, class packingT = canonical_packing_t<1>>
    using vector_t = Tensor<T, packingT, D>;

    // typedef for matrices
    template <int D1, int D2 = D1, typename T = real, class packingT = canonical_packing_t<2>>
    using matrix_t = Tensor<T, packingT, D1, D2>;

    // typedef for square matrices
    template <int D, typename T = real, class packingT = canonical_packing_t<2>>
    using square_matrix_t = matrix_t<D, D, T, packingT>;

    // typedef for symmetric matrices
    template <int D, typename T = real>
    using symmetric_matrix_t = matrix_t<D, D, T, symmetric_packing_t<2>>;

    // typedef for diagonal matrices
    template <int D, typename T = real>
    using diagonal_matrix_t = matrix_t<D, D, T, diagonal_packing_t<2>>;

    // typedef for fourth order tensors
    template <int D1, int D2 = D1, int D3 = D2, int D4 = D3, typename T = real>
    using fourth_order_tensor_t = Tensor<T, canonical_packing_t<4>, D1, D2, D3, D4>;

    // the zero tensor
    template <class tensorT>
    constexpr auto zero = make_zeros<tensorT>();

    // a tensor of ones
    template <class tensorT>
    constexpr auto ones = make_ones<tensorT>();

    // the identity tensor
    template <class tensorT>
    constexpr auto identity = make_identity<tensorT>();

    // the unit tensor with a one in the entry whose indices are specified in {J...}
    template <class tensorT, int... J>
    constexpr auto unit = make_basis_element<tensorT, J...>();

    // typedef for complex numbers
    using complex_t = std::complex<double>;

    // typedef for quaternions
    using quaternion_t = UnitQuaternion<complex_t>;

} // namespace pyre::tensor


#endif

// end of file
