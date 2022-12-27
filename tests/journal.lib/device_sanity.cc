// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>


// alias
using device_t = pyre::journal::device_t;


// the {device} class is abstract, so let's concretize
class Trivial : public device_t {
    // metmethods
public:
    ~Trivial();
    Trivial();

    // interface
public:
    virtual auto alert(const entry_type &) -> Trivial &;
    virtual auto help(const entry_type &) -> Trivial &;
    virtual auto memo(const entry_type &) -> Trivial &;
};


// metamethods
Trivial::~Trivial() {}
Trivial::Trivial() : device_t("trivial") {}

// the {alert} method
auto
Trivial::alert(const entry_type &) -> Trivial &
{
    // return myself
    return *this;
}


// the {help} method
auto
Trivial::help(const entry_type &) -> Trivial &
{
    // return myself
    return *this;
}


// and the {memo} method
auto
Trivial::memo(const entry_type &) -> Trivial &
{
    // return myself
    return *this;
}

// alias the type
using trivial_t = Trivial;


// exercise the trivial device
int
main()
{
    // instantiate
    trivial_t device;

    // make an entry
    trivial_t::entry_type entry;

    // record
    device.memo(entry);
    device.alert(entry);

    // all done
    return 0;
}


// end of file
