// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Index_h)
#define pyre_journal_Index_h


// owner of the map (channel name -> shared channel state), as well as the severity wide defaults
// each concrete {channel} maintains its own index as class data, shared among its instances
class pyre::journal::Index : public Inventory
{
    // types
public:
    // channel names
    using name_type = name_t;
    // shared state
    using inventory_type = Inventory;

    // the map from channel names to inventory instances
    using index_type = std::map<name_type, inventory_type>;

    // metamethods
public:
    inline Index(active_type active, fatal_type fatal);
    // let the compiler write the rest
    Index(const Index &) = default;
    Index(Index &&) = default;
    Index & operator= (const Index &) = default;
    Index & operator= (Index &&) = default;

    // interface
public:
    // simple access to the underlying index
    inline auto size() const;
    inline auto empty() const;
    inline auto contains(const name_type &) const;

    // explicit inventory insertion
    inline auto emplace(const name_type &, active_type, fatal_type);

    // iteration
    inline auto begin() const;
    inline auto end() const;

    // look up the shared state of a channel
    inline auto lookup(const name_type &) -> inventory_type &;

    // data members
private:
    index_type _index;
};


// get the inline definitions
#define pyre_journal_Index_icc
#include "Index.icc"
#undef pyre_journal_Index_icc


#endif

// end of file
