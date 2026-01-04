// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2026 all rights reserved


// code guard
#if !defined(pyre_tensor_forward_h)
#define pyre_tensor_forward_h


// set up the namespace
namespace pyre::tensor {

    // the tensor class
    template <typename T, class packingT, int... I>
    class Tensor;

    // alias for tensor
    template <typename T, class packingT, int... I>
    using tensor_t = Tensor<T, packingT, I...>;

    // the unit quaternion class
    template <typename T>
    class UnitQuaternion;

    // the zero tensor factory
    template <class tensorT>
    constexpr auto make_zeros() -> typename tensorT::diagonal_tensor_t;

    // the ones tensor factory
    template <class tensorT>
    constexpr auto make_ones() -> tensorT;

    // the identity tensor factory
    template <class tensorT>
    constexpr auto make_identity() -> typename tensorT::diagonal_tensor_t
        requires(tensorT::rank == 2);

    // returns whether the entries in a parameter pack {I...} are all equal
    template <int... I>
    constexpr auto entries_all_equal() -> bool;

    // the basis tensors factory (general version)
    template <class tensorT, int... I>
    constexpr auto make_basis_element() -> tensorT
        requires(
            sizeof...(I) == tensorT::rank &&
            // not a
            !(
                // diagonal entry
                entries_all_equal<I...>() &&
                // of a square tensor
                tensorT::is_square()));

    // the basis tensors factory (diagonal version)
    template <class tensorT, int... I>
    constexpr auto make_basis_element() -> typename tensorT::diagonal_tensor_t
        requires(
            sizeof...(I) == tensorT::rank &&
            // diagonal entry
            entries_all_equal<I...>() &&
            // of a square tensor
            tensorT::is_square());

} // namespace pyre::tensor


#endif

// end of file
