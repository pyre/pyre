// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// STL
#include <cassert>
#include <complex>
#include <cstdint>
#include <vector>
// support
#include <pyre/viz.h>


// check that the amplitude filter computes the magnitude of whatever cells it is handed: the
// absolute value of signed ones, the modulus of complex ones, and the cells themselves when
// they are unsigned, which have no absolute value of their own to ask for
template <typename cellT>
auto
check(const std::vector<cellT> & cells, const std::vector<double> & expected) -> void
{
    // my filter, over an iterator into the cells
    using amplitude_t =
        pyre::viz::iterators::filters::amplitude_t<typename std::vector<cellT>::const_iterator>;
    // make one at the start of the cells
    auto amplitude = amplitude_t(cells.cbegin());
    // go through the expected magnitudes
    for (auto value : expected) {
        // each one is what the filter reports for the cell under it
        assert(*amplitude == value);
        // on to the next cell
        ++amplitude;
    }
    // all done
    return;
}


// driver
int
main(int argc, char * argv[])
{
    // unsigned cells of every width are their own magnitudes
    check<std::uint8_t>({ 0, 7, 255 }, { 0, 7, 255 });
    check<std::uint16_t>({ 0, 7, 65535 }, { 0, 7, 65535 });
    check<std::uint32_t>({ 0, 7, 4294967295u }, { 0, 7, 4294967295.0 });
    check<std::uint64_t>({ 0, 7, 1ull << 40 }, { 0, 7, static_cast<double>(1ull << 40) });
    // signed cells lose their sign
    check<std::int16_t>({ -3, 0, 5 }, { 3, 0, 5 });
    check<std::int64_t>({ -(1ll << 40), 2 }, { static_cast<double>(1ll << 40), 2 });
    // floating point cells too
    check<double>({ -1.5, 2.25 }, { 1.5, 2.25 });
    // and complex cells report their modulus
    check<std::complex<float>>({ { 3, 4 }, { 0, -2 } }, { 5, 2 });
    // all done
    return 0;
}


// end of file
