// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_grid_Iterator_h)
#define pyre_grid_Iterator_h


// declaration
template <typename sliceT>
class pyre::grid::Iterator {
    // types
public:
    // my parts
    typedef sliceT slice_type;
    typedef typename slice_type::index_type index_type;
    typedef typename slice_type::packing_type packing_type;

    // meta-methods
public:
    Iterator(const slice_type & slice);
    Iterator(const index_type & current, const slice_type & slice);

    // interface
public:
    inline Iterator & operator++();
    inline const index_type & operator*() const;

    // implementation details
private:
    index_type _current;
    const slice_type & _slice;
};


#endif

// end of file
