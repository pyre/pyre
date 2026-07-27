// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the memory
#include <pyre/memory.h>


// type alias
using paged_t = pyre::memory::paged_t<double>;


// verify that misusing a paged store trips its firewalls
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("paged_oob");

    // silence the firewall
    pyre::journal::firewall_t::quiet();

    // the geometry
    paged_t::cell_count_type pageCells = 6;
    paged_t::cell_count_type pages = 4;
    // make a store
    paged_t store(pageCells, pages);

    // gingerly
    try {
        // reach past the end of the logical expanse
        store.at(store.cells());
        // unreachable
        throw std::logic_error("unreachable");
        // catch the firewall
    } catch (const pyre::journal::firewall_t::exception_type &) {
        // all good
    }

    // gingerly
    try {
        // ask about a page the table doesn't have
        store.resident(pages);
        // unreachable
        throw std::logic_error("unreachable");
        // catch the firewall
    } catch (const pyre::journal::firewall_t::exception_type &) {
        // all good
    }

    // gingerly
    try {
        // ask for the address of a page that was never brought in
        store.page(0);
        // unreachable
        throw std::logic_error("unreachable");
        // catch the firewall
    } catch (const pyre::journal::firewall_t::exception_type &) {
        // all good
    }

    // gingerly
    try {
        // claim there is content in a page that was never brought in
        store.validate(1);
        // unreachable
        throw std::logic_error("unreachable");
        // catch the firewall
    } catch (const pyre::journal::firewall_t::exception_type &) {
        // all good
    }

    // gingerly
    try {
        // claim to have written to a page that was never brought in
        store.taint(2);
        // unreachable
        throw std::logic_error("unreachable");
        // catch the firewall
    } catch (const pyre::journal::firewall_t::exception_type &) {
        // all good
    }

    // all done
    return 0;
}


// end of file
