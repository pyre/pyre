// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved


// code guard
#if !defined(pyre_tensor_concepts_h)
#define pyre_tensor_concepts_h


// set up the namespace
namespace pyre::tensor {

    // concept of a tensor
    template <class F>
    concept tensor_c = requires(F c) {
        // require that F only binds to {Tensor} specializations
        []<typename T, class packingT, int... I>(const Tensor<T, packingT, I...> &) {
        }(c);
    };

    // concept of a scalar
    template <class F>
    concept scalar_c = tensor_c<F> and F::size == 1;

    // concept of a vector
    template <class F>
    concept vector_c = tensor_c<F> and not scalar_c<F> and (F::rank == 1 || (F::rank == 2 && (F::dims[0] == 1 || F::dims[1] == 1)));

    // concept of a matrix
    template <class F>
    concept matrix_c =
        tensor_c<F> and not scalar_c<F> and F::rank == 2 and (F::dims[0] != 1 && F::dims[1] != 1);

    // concept of a square matrix
    template <class F>
    concept square_matrix_c = matrix_c<F> and F::dims[0] == F::dims[1];

    // concept of a diagonal matrix
    template <class F>
    concept diagonal_matrix_c = square_matrix_c<F> and F::diagonal;

} // namespace pyre::tensor


#endif

// end of file
