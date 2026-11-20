// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>

// the package under test
#include <pyre/postgres.h>
// support
#include <clocale>
// so a failing test can say why
#include <iostream>


// verify that real numbers are read and written the way postgres writes them, with a period
// before the fraction, whatever the locale of the program says about numbers
int
main()
{
    // pull in the names
    using namespace pyre::postgres;

    // switch to a locale that writes the fraction after a comma; on a machine that has none of
    // these, there is nothing this test can show
    if (std::setlocale(LC_NUMERIC, "de_DE.UTF-8") == nullptr
        && std::setlocale(LC_NUMERIC, "de_DE.utf8") == nullptr
        && std::setlocale(LC_NUMERIC, "fr_FR.UTF-8") == nullptr) {
        // so leave quietly
        return 0;
    }

    // the text of a real number as the server writes it reads as that number
    if (decode<double>("1.5") != 1.5) {
        std::cerr << "'1.5' did not read as 1.5 in a comma locale" << std::endl;
        return 1;
    }
    // and a real number goes out in the server's spelling
    const auto text = encode(1.5);
    if (!text.has_value() || *text != "1.5") {
        std::cerr << "1.5 was written as '" << text.value_or("NULL") << "' in a comma locale"
                  << std::endl;
        return 1;
    }

    // all done
    return 0;
}


// end of file
