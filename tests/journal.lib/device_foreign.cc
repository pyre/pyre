// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>

// type aliases
using device_t = pyre::journal::device_t;
using trash_t = pyre::journal::trash_t;
using splitter_t = pyre::journal::splitter_t;


// a device that counts the entries it is handed, and says whether it is foreign
class Counter : public device_t {
    // metamethods
public:
    // a counter that is native unless told otherwise
    Counter(bool foreign = false) : device_t("counter"), entries(0), _foreign(foreign) {}
    // destructor
    ~Counter() {}

    // interface
public:
    // count user facing messages
    virtual auto alert(const entry_type &) -> Counter &
    {
        // one more
        ++entries;
        // all done
        return *this;
    }
    // count help screens
    virtual auto help(const entry_type &) -> Counter &
    {
        // one more
        ++entries;
        // all done
        return *this;
    }
    // count developer messages
    virtual auto memo(const entry_type &) -> Counter &
    {
        // one more
        ++entries;
        // all done
        return *this;
    }
    // whether i claim to be implemented outside c++
    virtual auto foreign() const -> bool
    {
        // as told
        return _foreign;
    }

    // data
public:
    // the number of entries i was handed
    int entries;

private:
    // whether i am foreign
    bool _foreign;
};


// verify that devices are native unless they say otherwise
int
main()
{
    // the stock devices are native
    assert(trash_t().foreign() == false);
    assert(splitter_t().foreign() == false);
    // as is a client device that does not say otherwise
    assert(Counter().foreign() == false);
    // but a client device can claim to be foreign
    assert(Counter(true).foreign() == true);
    // all done
    return 0;
}


// end of file
