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
using chronicler_t = pyre::journal::chronicler_t;
using cout_t = pyre::journal::cout_t;


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


// verify that a foreign default device is replaced by a console, and a native one is kept
int
main()
{
    // make a native device
    auto native = std::make_shared<Counter>();
    // install it as the default
    chronicler_t::device(native);
    // detach the foreign devices
    chronicler_t::detachForeign();
    // the native device is still the default
    assert(chronicler_t::device() == native);

    // make a foreign device
    auto foreign = std::make_shared<Counter>(true);
    // install it as the default
    chronicler_t::device(foreign);
    // detach the foreign devices
    chronicler_t::detachForeign();
    // the default is now a console
    assert(std::dynamic_pointer_cast<cout_t>(chronicler_t::device()));
    // and nothing in the journal holds the foreign device any more
    assert(foreign.use_count() == 1);
    // all done
    return 0;
}


// end of file
