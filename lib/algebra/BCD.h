// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//

#if !defined(pyre_algebra_BCD_h)
#define pyre_algebra_BCD_h


namespace pyre {
    namespace algebra {
        template <size_t scale, typename precision_t=long> class BCD;
    }
}


// the BCD class
template <size_t scale, typename precision_t>
class pyre::algebra::BCD {
    // interface
public:

    // convert to double
    operator double () const;

    // meta methods
public:
    inline ~BCD();

    inline BCD(precision_t msw=0, precision_t lsw=0);
    BCD(const BCD &);
    const BCD & operator= (const BCD &);

    // data members
public:
    precision_t _msw;
    precision_t _lsw;

    static const size_t _scale = scale;

};


// get the inline definitions
#define pyre_algebra_BCD_icc
#include "BCD.icc"
#undef pyre_algebra_BCD_icc


#endif

// end of file
