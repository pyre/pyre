// -*- javascript -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// singleton
var configuration;

// when the page is done loading...
$(document).ready(
    // invoke this function
    function() {
        // build a configuration object
        configuration = new pyre_Configuration("#pyre-configuration");

        // issue a request for the current configuration
        $.ajax({
            url: "/boot"
        }).done(function(data) {
            configuration.receive(data);
        });

        // and get back to listening to the user
        return;
    }
);

// end of file
