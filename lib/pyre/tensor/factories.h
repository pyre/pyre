// code guard
#if !defined(pyre_tensor_factories_h)
#define pyre_tensor_factories_h


namespace pyre::tensor {

    // returns whether the entries in a parameter pack {I...} are all equal
    template <int... I>
    constexpr auto entries_all_equal() -> bool
    {
        // store the template parameter pack in an array for convenience
        constexpr std::array<int, sizeof...(I)> index { I... };

        // helper function to check whether all entries in {index} are equal
        constexpr auto _entries_all_equal = [index]<int... J>(integer_sequence<J...>)
        {
            // if all entries in the index are equal
            if constexpr (((index[J] == index[J + 1]) && ...)) {
                // then the index is diagonal
                return true;
            }
            // then the index is not diagonal
            return false;
        };

        // trivial case: there is only one index
        if (index.size() == 1)
            return false;

        // otherwise check if all the indices are equal
        return _entries_all_equal(make_integer_sequence<sizeof...(I) - 1> {});
    }

    template <class tensorT>
    constexpr auto make_zeros() -> tensorT::diagonal_tensor_t
    {
        constexpr auto _make_zeros =
            []<int... J>(integer_sequence<J...>)->tensorT::diagonal_tensor_t
        {
            constexpr auto fill_zeros = []<int>() consteval->tensorT::type
            {
                return 0;
            };
            // return a tensor filled with zeros
            return typename tensorT::diagonal_tensor_t(fill_zeros.template operator()<J>()...);
        };

        // fill tensor with zeros
        return _make_zeros(make_integer_sequence<tensorT::diagonal_tensor_t::size> {});
    }

    template <class tensorT>
    constexpr auto make_ones() -> tensorT
    {
        constexpr auto _make_ones = []<int... J>(integer_sequence<J...>)->tensorT
        {
            constexpr auto fill_ones = []<int>() consteval->tensorT::type
            {
                return 1;
            };
            // return a tensor filled with ones
            return tensorT(fill_ones.template operator()<J>()...);
        };

        // fill tensor with ones
        return _make_ones(make_integer_sequence<tensorT::size> {});
    }

    namespace {
        template <class tensorT, int... I>
        constexpr auto make_basis_element_implementation() -> tensorT
        {
            // typedef for index type
            using index_t = tensorT::index_t;
            // wrap the parameter pack into an index
            index_t index(I...);

            // make an element of the basis by the Kronecker delta
            constexpr auto _make_basis_element =
                []<int... J>(index_t K, integer_sequence<J...>)->tensorT
            {
                constexpr auto delta = [](int II, int JJ) -> tensorT::type {
                    if (II == JJ)
                        return 1;
                    return 0;
                };

                // fill tensor with delta_ij
                return tensorT(delta(tensorT::layout()[K] /* I */, J)...);
            };

            return _make_basis_element(index, make_integer_sequence<tensorT::size> {});
        }
    } // namespace

    // make the element of the tensor basis that has a one at the index given by {I...}
    template <class tensorT, int... I>
    constexpr auto make_basis_element() -> tensorT
        requires(
            sizeof...(I) == tensorT::rank &&
            // not a
            !(
                // diagonal entry
                entries_all_equal<I...>() &&
                // of a square tensor
                tensorT::is_square()))
    {
        // return the requested element of the basis (non-diagonal version, returns a full tensor)
        return make_basis_element_implementation<tensorT, I...>();
    }

    // make the element of the tensor basis that has a one at the index given by {I...}
    //  (diagonal version: index is on diagonal and tensor is square)
    template <class tensorT, int... I>
    constexpr auto make_basis_element() -> tensorT::diagonal_tensor_t
        requires(
            sizeof...(I) == tensorT::rank &&
            // diagonal entry
            entries_all_equal<I...>() &&
            // of a square tensor
            tensorT::is_square())
    {
        // return the requested element of the basis (diagonal version, returns a diagonal tensor)
        return make_basis_element_implementation<typename tensorT::diagonal_tensor_t, I...>();
    }

    // factory for identity tensor (for now only for second order tensors)
    template <class tensorT>
    static constexpr auto make_identity() -> tensorT::diagonal_tensor_t
        requires(tensorT::rank == 2)
    {
        constexpr auto _make_ones = []<int... J>(integer_sequence<J...>)->tensorT::diagonal_tensor_t
        {
            constexpr auto fill_ones = []<int>() consteval->tensorT::type
            {
                return 1;
            };
            // return a tensor filled with zeros
            return typename tensorT::diagonal_tensor_t(fill_ones.template operator()<J>()...);
        };

        // fill tensor with zeros
        return _make_ones(make_integer_sequence<tensorT::diagonal_tensor_t::size> {});
    }
} // namespace pyre::tensor


#endif

// end of file
