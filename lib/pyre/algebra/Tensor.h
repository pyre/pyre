// -*- C++ -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//


#if !defined(pyre_algebra_Tensor_h)
#define pyre_algebra_Tensor_h


namespace pyre::algebra {
    template <typename T, class packingT, int... I>
    class Tensor {
      private:
        // layout
        // static constexpr pack_t _layout {{I ...}, index_t::zero(), pack_t::order_type::rowMajor()};
        static constexpr packingT _layout { {I ...} };
        // rank of the tensor (N = 0 for empty parameter pack, i.e. scalar)
        static constexpr int N = sizeof...(I);
        // number of total entries of the tensor (S = 1 for empty parameter pack, i.e. scalar)
        static constexpr auto S = 
            // if it is not a diagonal packing
            !std::is_same_v<packingT, pyre::grid::diagonal_t<N>> ? 
            // get the answer from the layout
            _layout.cells() 
            // otherwise, get the answer from the layout but do not count the trailing zero
            : _layout.cells() - 1; 

      private:
        // the packing strategy
        using pack_t = packingT;
        // index
        using index_t = typename pack_t::index_type;
        // of T on the heap
        using storage_t = typename pyre::memory::stack_t< _layout.cells() , T>;
        // data type
        using data_t = storage_t;

      public:
        // export the underlying type
        using type = T;
        // export the rank
        static constexpr int dofs = N;
        // export the container size
        static constexpr int size = S;

      public:
        // default constructor
        constexpr Tensor();

        // constructor with underlying data type
        constexpr Tensor(const data_t &);

        // constructor with underlying data type (need this for return value optimization)
        constexpr Tensor(const data_t &&);

        // constructor from brace-enclosed initializer list
        template <class... T2>
        constexpr Tensor(T2...) requires(sizeof...(T2) == S);

        // copy constructor
        constexpr Tensor(const Tensor &) = default;

        // move constructor
        constexpr Tensor(Tensor &&) = default;

        // copy assignment operator
        constexpr Tensor & operator=(const Tensor &) = default;

        // move assignment operator
        constexpr Tensor & operator=(Tensor &&) = default;

        // destructor
        constexpr ~Tensor();

      public:
        // components accessors with index
        constexpr const T & operator[](index_t) const;
        constexpr T & operator[](index_t);

        // components accessors with integers
        constexpr const T & operator[](int) const;
        constexpr T & operator[](int);

        // cast to underlying type T (enable if S = 1, i.e. scalar)
        constexpr operator T() const requires(S == 1);

        // cast to underlying data structure
        constexpr operator data_t() const;

        // cast to canonical packing
        constexpr operator Tensor<T, pyre::grid::canonical_t<N>, I...>() const; 

        // cast to symmetric packing (enable only for diagonal packing)
        constexpr operator Tensor<T, pyre::grid::symmetric_t<N>, I...>() const requires 
            (std::is_same_v<packingT, pyre::grid::diagonal_t<N>>); 

        // support for ranged for loops
        constexpr const auto begin() const;
        constexpr const auto end() const;

        // reset all entries to zero
        constexpr void reset();

        // get shape of tensor
        constexpr auto shape() const;

        // checks if the tensor is symmetric
        constexpr bool is_symmetric() const;

        // checks if the tensor is diagonal
        constexpr bool is_diagonal() const;

      private:
        // helper function for index sequence
        template <size_t... J, class... T2>
        constexpr void _initialize(std::index_sequence<J...>, T2...);

        // helper function for index sequence
        template <size_t... J>
        constexpr void _reset(std::index_sequence<J...>);

        // helper function to build the zero tensor
        template <size_t... J>
        static constexpr pyre::algebra::Tensor<T, packingT, I...> 
            _make_zeros(std::index_sequence<J...>);

        // helper function to build a tensor of ones
        template <size_t... J>
        static constexpr pyre::algebra::Tensor<T, packingT, I...> 
            _make_ones(std::index_sequence<J...>);

        // helper function to build a tensor of zeros with a 1 at index K
        template <size_t... J>
        static constexpr pyre::algebra::Tensor<T, packingT, I...> 
            _make_basis_element(index_t, std::index_sequence<J...>);

      public:
        // the zero element
        static constexpr Tensor<T, packingT, I...> zero = 
            pyre::algebra::Tensor<T, packingT, I...>::_make_zeros(
            std::make_index_sequence<pyre::algebra::Tensor<T, packingT, I...>::size> {});

        // a tensor of ones
        static constexpr Tensor<T, packingT, I...> one = 
            pyre::algebra::Tensor<T, packingT, I...>::_make_ones(
            std::make_index_sequence<pyre::algebra::Tensor<T, packingT, I...>::size> {});

        // the K-th unit tensor
        template<typename... Args>
        static constexpr Tensor<T, packingT, I...> unit(Args...) requires (sizeof...(Args) == N);

      // accessors
      public:
        static constexpr const packingT & layout() {return _layout;}

      private:
        // data
        data_t _data;
    };
}


// get the inline definitions
#define pyre_algebra_Tensor_icc
#include "Tensor.icc"
#undef pyre_algebra_Tensor_icc


#endif

// end of file
