// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Detail_h)
#define pyre_journal_Detail_h


// control over the level of detail
class pyre::journal::Detail {
    // types
public:
    // the detail level
    using detail_type = detail_t;

    // metamethods
public:
    // constructor
    inline explicit Detail(detail_type);

    // interface
public:
    // accessors
    inline auto detail() const -> detail_type;

    // data
private:
    const detail_type _detail;
};


// get the inline definitions
#define pyre_journal_Detail_icc
#include "Detail.icc"
#undef pyre_journal_Detail_icc


#endif

// end of file
