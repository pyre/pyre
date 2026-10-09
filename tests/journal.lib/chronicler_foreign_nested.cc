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


// verify that foreign devices are detached from splitters at any depth, and that a splitter
// attached to itself does not trap the walk
int
main()
{
    // make a foreign device and a native one
    auto foreign = std::make_shared<Counter>(true);
    auto native = std::make_shared<Counter>();
    // make an inner splitter over both
    auto inner = std::make_shared<splitter_t>();
    // attach them
    inner->attach(foreign).attach(native);
    // make an outer splitter over the inner one and the foreign device
    auto outer = std::make_shared<splitter_t>();
    // attach them, and the outer splitter to itself
    outer->attach(inner).attach(foreign).attach(outer);
    // install the outer splitter as the default
    chronicler_t::device(outer);

    // detach the foreign devices
    chronicler_t::detachForeign();

    // the outer splitter is still the default
    assert(chronicler_t::device() == outer);
    // and holds the inner splitter and itself
    assert(outer->outputs().size() == 2);
    assert(outer->outputs()[0] == inner);
    assert(outer->outputs()[1] == outer);
    // the inner splitter holds only the native device
    assert(inner->outputs().size() == 1);
    assert(inner->outputs()[0] == native);
    // and nothing in the journal holds the foreign device any more
    assert(foreign.use_count() == 1);

    // break the cycle, so the splitters can be destroyed
    outer->detach(outer);
    // all done
    return 0;
}


// end of file
