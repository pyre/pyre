// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved


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
    concept vector_c = tensor_c<F> and F::rank == 1;

    // concept of a matrix
    template <class F>
    concept matrix_c = tensor_c<F> and F::rank == 2;

    // concept of a square matrix
    template <class F>
    concept square_matrix_c = matrix_c<F> and F::dims[0] == F::dims[1];

    // concept of a diagonal matrix
    template <class F>
    concept diagonal_matrix_c = square_matrix_c<F> and F::diagonal;

    // concept of a symmetric matrix
    template <class F>
    concept symmetric_matrix_c = square_matrix_c<F> and F::symmetric;

    // concept of two tensors having the same shape
    template <class F1, class F2>
    concept tensor_same_shape_c = tensor_c<F1> and tensor_c<F2> and F1::dims == F2::dims;

    // concept of a fourth-order tensor
    template <class F>
    concept fourth_order_tensor_c = tensor_c<F> and F::rank == 4;

    // concept of a compatible pair of tensors
    // (an instance of {tensorT1} can be assigned to an instance of {tensorT2})
    template <class tensorT1, class tensorT2>
    concept compatible_tensor_c =
        tensor_c<tensorT1> and tensor_c<tensorT2>
        and std::is_same_v<
            typename repacking_sum<
                typename tensorT1::pack_t, typename tensorT2::pack_t>::packing_type,
            typename tensorT2::pack_t>;

} // namespace pyre::tensor


#endif

// end of file
