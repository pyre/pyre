// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// verify that we can create two proxies to the same shared inventory and manipulate the
// shared state through either one


// the journal
#include <pyre/journal.h>
// support
#include <cassert>


// convenience
template <class clientT>
using proxy_t = pyre::journal::inventory_proxy_t<clientT>;


// a client stub; the proxy relies on {crtp} to enable chaining
class channel_t : public proxy_t<channel_t>
{
    // type aliases
public:
    using proxy_type = proxy_t<channel_t>;
    using inventory_type = typename proxy_type::inventory_type;
    using inventory_reference = typename proxy_type::inventory_reference;
    // the map from channel names to inventories
    using index_type = pyre::journal::index_t;
    using index_reference = index_type &;

    // metamethods
public:
    inline channel_t(inventory_reference inventory) :
        proxy_type(inventory)
    {}

    // static interface
public:
    // access to the severity wide index with the default settings and the names of the channels
    inline static auto index() -> index_reference;

    // implementation details: static data
private:
    static index_type _index;
};

// static interface
auto channel_t::index() -> index_reference { return _index; }
// static data
channel_t::index_type channel_t::_index { true, false };


// verify that we can manipulate the inventory state through a proxy
int main() {
    // make the shared inventory instance
    channel_t::inventory_type inventory(true, false);
    // create a channel
    channel_t ch_1(inventory);
    // check that the client sees the state of the inventory
    assert (ch_1.device() == pyre::journal::chronicler_t::device());

    // create another channel with access to the shared state
    channel_t ch_2(inventory);
    // it should also see the same device
    assert (ch_2.device() == ch_1.device());

    // install a custom device in the shared state
    inventory.device<pyre::journal::trash_t>();

    // check again
    assert (ch_1.device() == inventory.device());
    assert (ch_2.device() == ch_1.device());

    // all done
    return 0;
}


// end of file
