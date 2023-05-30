// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved


// code guard
#if !defined(pyre_tensor_api_h)
#define pyre_tensor_api_h


// low level entities; you should probably stay away from them
namespace pyre::tensor {
    // typedef for real values
    using real = double;

    // typedef for scalars
    using scalar_t = real;

    // typedef for vectors
    template <int D, typename T = real, class packingT = pyre::grid::canonical_t<1>>
    using vector_t = pyre::tensor::Tensor<T, packingT, D>;

    // typedef for matrices
    template <int D1, int D2 = D1, typename T = real, class packingT = pyre::grid::canonical_t<2>>
    using matrix_t = pyre::tensor::Tensor<T, packingT, D1, D2>;

    // typedef for symmetric matrices
    template <int D, typename T = real>
    using symmetric_matrix_t = matrix_t<D, D, T, pyre::grid::symmetric_t<2>>;

    // typedef for diagonal matrices
    template <int D, typename T = real>
    using diagonal_matrix_t = matrix_t<D, D, T, pyre::grid::diagonal_t<2>>;
} // namespace pyre::tensor


#endif

// end of file
