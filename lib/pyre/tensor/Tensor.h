// -*- C++ -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved
//


#if !defined(pyre_tensor_Tensor_h)
#define pyre_tensor_Tensor_h


namespace pyre::tensor {
    template <typename T, class packingT, int... I>
    class Tensor {
    private:
        // layout
        static constexpr packingT _layout { { I... } };
        // rank of the tensor (N = 0 for empty parameter pack, i.e. scalar)
        static constexpr int N = sizeof...(I);
        // number of total entries of the tensor (S = 1 for empty parameter pack, i.e. scalar)
        static constexpr auto S =
            // if it is not a diagonal packing
            !std::is_same_v<packingT, pyre::grid::diagonal_t<N>> ?
                // get the answer from the layout
                _layout.cells()
                // otherwise, get the answer from the layout but do not count the trailing zero
                :
                _layout.cells() - 1;

    public:
        // export my type
        using tensor_t = Tensor<T, packingT, I...>;
        // export a canonical tensor with my same underlying type {T} and shape {I...}
        using canonical_tensor_t = Tensor<T, pyre::grid::canonical_t<N>, I...>;
        // export a symmetric tensor with my same underlying type {T} and shape {I...}
        using symmetric_tensor_t = Tensor<T, pyre::grid::symmetric_t<N>, I...>;
        // export a diagonal tensor with my same underlying type {T} and shape {I...}
        using diagonal_tensor_t = Tensor<T, pyre::grid::diagonal_t<N>, I...>;
        // export the packing strategy
        using pack_t = packingT;
        // export the index type
        using index_t = typename pack_t::index_type;
        // export the storage type (T on the stack)
        using storage_t = typename pyre::memory::stack_t<_layout.cells(), T>;
        // export data type
        using data_t = storage_t;
        // export the underlying type
        using scalar_type = T;
        // export the rank
        static constexpr int rank = N;
        // export the container size
        static constexpr int size = S;
        // export whether the tensor is symmetric
        static constexpr bool symmetric = std::is_same_v<packingT, pyre::grid::symmetric_t<N>>
                                       || std::is_same_v<packingT, pyre::grid::diagonal_t<N>>;
        // export whether the tensor is diagonal
        static constexpr bool diagonal = std::is_same_v<packingT, pyre::grid::diagonal_t<N>>;
        // dimensions (the maximum index value for each index)
        static constexpr std::array<int, N> dims { I... };

    public:
        // default constructor
        constexpr Tensor();

        // constructor with underlying data type
        constexpr Tensor(const data_t &);

        // constructor with underlying data type (need this for return value optimization)
        constexpr Tensor(data_t &&) noexcept;

        // constructor from parameter pack
        template <class... T2>
        constexpr Tensor(T2...)
            requires(sizeof...(T2) == S);

        // constructor from brace-enclosed initializer list
        template <class T2>
        constexpr Tensor(T2 (&&)[S]);

        // copy constructor from a tensor with (potentially) different packing
        template <tensor_c tensorT>
        constexpr Tensor(const tensorT & rhs)
            requires(compatible_tensor_c<tensorT, tensor_t>);

        // move constructor from a tensor with exact same packing
        template <tensor_c tensorT>
        constexpr Tensor(tensorT &&)
            requires(std::is_same_v<tensor_t, tensorT>);

        // copy assignment operator from a tensor with (potentially) different packing
        template <tensor_c tensorT>
        constexpr Tensor & operator=(const tensorT & rhs)
            requires(compatible_tensor_c<tensorT, tensor_t>);

        // move assignment operator from a tensor with exact same packing
        template <tensor_c tensorT>
        constexpr Tensor & operator=(tensorT &&)
            requires(std::is_same_v<tensor_t, tensorT>);

        // destructor
        constexpr ~Tensor();

    public:
        // components accessors with index
        constexpr const T & operator[](index_t) const;
        constexpr T & operator[](index_t);

        // components accessors with integers
        constexpr const T & operator[](int) const;
        constexpr T & operator[](int);

        // takes a parameter pack {J...} and evaluates (at compile time) the offset corresponding
        // to the entry identified by the {J...} indices, based on the tensor packing
        template <int... J>
        static consteval auto getOffset() -> int
        {
            return _layout.offset({ J... });
        }

        // cast to atomic type T (enable the tensor is a scalar)
        constexpr operator T() const
            requires(scalar_c<tensor_t>);

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

        // checks if the layout is square
        static constexpr bool is_square();

    private:
        // helper function for index sequence
        template <int... J, class... T2>
        constexpr void _initialize(integer_sequence<J...>, T2...);

        // helper function for index sequence
        template <int... J, class T2>
        constexpr void _initialize(integer_sequence<J...>, T2 (&)[S]);

        // helper function for index sequence
        template <int... J>
        constexpr void _reset(integer_sequence<J...>);

        // accessors
    public:
        static constexpr const packingT & layout() { return _layout; }

    private:
        // data
        data_t _data;
    };
} // namespace pyre::tensor


// get the inline definitions
#define pyre_tensor_Tensor_icc
#include "Tensor.icc"
#undef pyre_tensor_Tensor_icc


#endif

// end of file
