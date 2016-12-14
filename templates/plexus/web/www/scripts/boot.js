// -*- javascript -*-
// -*- coding: utf-8 -*-
//
// authors:
//   {project.authors}
//
// (c) {project.span} all rights reserved
//

// singleton
var configuration;

// when the page is done loading...
$(document).ready(
    // invoke this function
    function() {{
        // build a configuration object
        configuration = new {project.name}_Configuration("#{project.name}-configuration");

        // action elements submit ajax requests to the server
        $("[action]").click(submitAction);

        // input elements mark the model as dirty when they change
        $("td.field > input").change(updateModel);

        // issue a request for the current configuration
        $.ajax({{
            url: "/send"
        }}).done(function(data) {{
            configuration.receive(data);
        }});

        // and get back to listening to the user
        return;
    }}
);

// end of file
