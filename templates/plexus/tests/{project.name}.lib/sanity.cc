// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// get the journal
#include <pyre/journal.h>
// get the {{{project.name}}} version
#include <{project.name}/version.h>


// the driver
int main(int argc, char *argv[])
{{
    // configure journal
    pyre::journal::application("sanity");
    pyre::journal::init(argc, argv);

    // make a channel
    auto channel = pyre::journal::debug_t("{project.name}.sanity");

    // get the {{{project.name}}} version
    auto version = {project.name}::version::version();

    // say something
    channel
        << "version: " << pyre::journal::newline
        // the static version, straight from the headers
        << "   static: "
        << {project.name}::version::major << "."
        << {project.name}::version::minor << "."
        << {project.name}::version::micro << "."
        << {project.name}::version::revision << pyre::journal::newline
        // the dynamic version, from the library
        << "  dynamic: "
        << version.major << "."
        << version.minor << "."
        << version.micro << "."
        << version.revision << "."
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}}


// end of file
