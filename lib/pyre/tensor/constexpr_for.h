// -*- c++ -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved


// code guard
#if !defined(pyre_tensor_constexpr_for_h)
#define pyre_tensor_constexpr_for_h


namespace pyre::tensor {

    // constexpr for loop calling function f(i) for each i in (Start, End)
    template <int End, int Index1 = 0, class F>
    constexpr void constexpr_for_1(F && f)
    {
        if constexpr (Index1 < End) {
            f.template operator()<Index1>();
            return constexpr_for_1<End, Index1 + 1>(f);
        }
    }

    // take f(i, j) and return f_I(j) := f(I, j) for I fixed
    template <int I, class F>
    constexpr auto f_I(F && f)
    {
        return [f]<int j>() {
            f.template operator()<I, j>();
        };
    }

    // constexpr for loop calling function f(i, j) for each i,j in (Start, End)x(Start, End)
    template <int End1, int End2, int Index1 = 0, class F>
    constexpr void _constexpr_for_2(F && f)
    {
        if constexpr (Index1 < End1) {
            constexpr_for_1<End2>(f_I<Index1>(f));
            _constexpr_for_2<End1, End2, Index1 + 1>(f);
        }

        // the above expands to the following for Start=0, End=3:
        // constexpr_for_1<Start, End>(f_I<0>(f));
        // constexpr_for_1<Start, End>(f_I<1>(f));
        // constexpr_for_1<Start, End>(f_I<2>(f));
    }

    template <int End1, int End2, class F>
    constexpr void constexpr_for_2(F && f)
    {
        _constexpr_for_2<End1, End2, 0>(f);
    }

    // take f(i, j, k) and return f_IJ(k) := f(I, J, k) for I, J fixed
    template <int I, class F>
    constexpr auto f_IJ(F && f)
    {
        return [f]<int j, int k>() {
            f.template operator()<I, j, k>();
        };
    }

    // constexpr for loop calling function f(i, j, j) for each i,j,k in (Start, End)x(Start, End)
    template <int End1, int End2, int End3, int Index1 = 0, int Index2 = 0, class F>
    constexpr void _constexpr_for_3(F && f)
    {
        if constexpr (Index1 < End1) {
            constexpr_for_2<End2, End3>(f_IJ<Index1>(f));
            _constexpr_for_3<End1, End2, End3, Index1 + 1, Index2>(f);
        }
    }

    template <int End1, int End2, int End3, class F>
    constexpr void constexpr_for_3(F && f)
    {
        _constexpr_for_3<End1, End2, End3, 0, 0>(f);
    }

    // take f(i, j, k, l) and return f_IJK(l) := f(I, J, K, l) for I, J, K fixed
    template <int I, class F>
    constexpr auto f_IJK(F && f)
    {
        return [f]<int j, int k, int l>() {
            f.template operator()<I, j, k, l>();
        };
    }

    // constexpr for loop calling function f(i, j, k, l) for each i,j,k,l in (Start, End)x(Start,
    // End)
    template <
        int End1, int End2, int End3, int End4, int Index1 = 0, int Index2 = 0, int Index3 = 0,
        class F>
    constexpr void _constexpr_for_4(F && f)
    {
        if constexpr (Index1 < End1) {
            constexpr_for_3<End2, End3, End4>(f_IJK<Index1>(f));
            _constexpr_for_4<End1, End2, End3, End4, Index1 + 1, Index2, Index3>(f);
        }
    }

    template <int End1, int End2, int End3, int End4, class F>
    constexpr void constexpr_for_4(F && f)
    {
        _constexpr_for_4<End1, End2, End3, End4, 0, 0>(f);
    }

} // namespace pyre::tensor


#endif

// end of file
