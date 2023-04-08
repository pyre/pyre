// code guard
#if !defined(pyre_algebra_factories_h)
#define pyre_algebra_factories_h


namespace pyre::algebra {
    
    template <int S /*size of tensor*/, typename T, class packingT, int... I>
    constexpr auto make_zeros() 
        -> pyre::algebra::Tensor<T, packingT, I...>
    {
        using tensor_t = pyre::algebra::Tensor<T, packingT, I...>;

        constexpr auto _make_zeros = []<size_t... J>(std::index_sequence<J...>) 
            -> tensor_t
        {
            constexpr auto fill_zeros = []<size_t>() consteval-> T { return 0; };
            // return a tensor filled with ones
            return tensor_t(fill_zeros.template operator()<J>()...);
        };

        // fill tensor with zeros
        return _make_zeros(std::make_index_sequence<S>{});
    }

    template <int S /*size of tensor*/, typename T, class packingT, int... I>
    constexpr auto make_ones() 
        -> pyre::algebra::Tensor<T, packingT, I...> 
    {
        using tensor_t = pyre::algebra::Tensor<T, packingT, I...>;

        constexpr auto _make_ones = []<size_t... J>(std::index_sequence<J...>) 
            -> tensor_t
        {
            constexpr auto fill_ones = []<size_t>() consteval-> T { return 1; };
            // return a tensor filled with ones
            return tensor_t(fill_ones.template operator()<J>()...);
        };

        // fill tensor with ones
        return _make_ones(std::make_index_sequence<S>{});
    }

    // make the element of the tensor basis that has a one at the index given by {args...}
    template <int S, typename T, class packingT, int... I>
    constexpr auto make_basis_element(auto index
        // if should be /*pyre::algebra::Tensor<T, packingT, I...>::index_t index*/ but for some 
        //  reason it gives a compiler error
        )
        -> pyre::algebra::Tensor<T, packingT, I...>
    {
        // typedef for tensor type and index type
        using tensor_t = pyre::algebra::Tensor<T, packingT, I...>;
        using index_t = tensor_t::index_t;

        constexpr auto _make_basis_element = []<size_t... J>(index_t K, std::index_sequence<J...>) 
            -> tensor_t
        {
            constexpr auto delta = [](size_t II, size_t JJ) ->T 
            { 
                if (II == JJ) return 1; 
                return 0;
            };

            // fill tensor with delta_ij
            return tensor_t(delta(pyre::algebra::Tensor<T, packingT, I...>::layout()[K] /* I */, J)...);
        };

        return _make_basis_element(index, std::make_index_sequence<S>{});
    }
}


#endif

// end of file
