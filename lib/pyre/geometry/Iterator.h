// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_geometry_Iterator_h)
#define pyre_geometry_Iterator_h


// declaration
template <typename indexT, typename orderT>
class pyre::geometry::Iterator {
    // types
public:
    // my parts
    typedef indexT index_type;
    typedef orderT order_type;

    // meta-methods
public:
    Iterator(const index_type & begin, const index_type & end, const order_type & order);

    // interface
public:
    inline Iterator & operator++();
    inline const index_type & operator*() const;

    // access to my limits
    const index_type & begin() const;
    const index_type & end() const;

    // implementation details
private:
    index_type _current;
    const index_type _begin;
    const index_type _end;
    const order_type _order;
};


#endif

// end of file
