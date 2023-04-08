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
        // static constexpr packingT _layout {{I ...}, index_t::zero(), pack_t::order_type::rowMajor()};
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

      public:
        // export the packing strategy
        using pack_t = packingT;
        // export the index type
        using index_t = typename pack_t::index_type;
        // export the storage type (T on the stack)
        using storage_t = typename pyre::memory::stack_t< _layout.cells() , T>;
        // export data type
        using data_t = storage_t;
        // export the underlying type
        using type = T;
        // export the order
        static constexpr int order = N;
        // export the container size
        static constexpr int size = S;
        // TOFIX: export my type here Tensor<...>

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
        constexpr auto begin();
        constexpr auto end();

        // reset all entries to zero
        constexpr void reset();

        // get shape of tensor
        constexpr auto shape() const;

        // checks if the packing is symmetric
        constexpr bool is_symmetric() const;

        // checks if the packing is diagonal
        constexpr bool is_diagonal() const;

      private:
        // helper function for index sequence
        template <size_t... J, class... T2>
        constexpr void _initialize(std::index_sequence<J...>, T2...);

        // helper function for index sequence
        template <size_t... J>
        constexpr void _reset(std::index_sequence<J...>);

        // TOFIX: from index sequence to integer sequence

        // TOFIX convert all these to the -> syntax

      public:
        // the zero tensor // TOFIX: this should be a diagonal tensor
        static constexpr Tensor<T, packingT, I...> zero = 
            make_zeros<size, T, packingT, I...>();

        // a tensor of ones // TOFIX: call this {ones}
        static constexpr Tensor<T, packingT, I...> one = 
            make_ones<size, T, packingT, I...>();

        // TOFIX: this should really take in input an index_T
        // the unit tensor with a one in the entry whose indices are specified in {Args...} 
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
