// -*- javascript -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// pyre configuration object
// constructor
function pyre_Configuration(name) {
    // locate the configuration placeholder
    this.element = $(name)

    // make something up
    value = this.buildControls();
    // install
    this.element.html(value);

    // all done
    return
}

// state
pyre_Configuration.prototype.dirty = false;

// build the configuration controls
pyre_Configuration.prototype.buildControls = function() {
    // the control box is an itemized list
    box = [
        //
        // actions
        '<p>',
        '<table class="pyre-actions">',

        // all done with the actions
        '</table>',
        '</p>',

        // all done
    ];

    // assemble it
    body = box.join("");
    // all done
    return body;
}

// behavior
pyre_Configuration.prototype.close = function() {
    // close the current tab
    window.close();
    // prevent event bubbling
    return false;
}

pyre_Configuration.prototype.receive = function(data) {
    // show me
    console.log("retrieved initial configuration");
    // save the data model
    this.model = $.parseJSON(data);
    // mark it as clean
    this.dirty = false;

    // update
    console.log("painting the view with the data model");

    // all done
    return;
}


updateModel = function() {
    // save me
    var self = $(this);
    // who am i?
    var name = self.attr("name");
    // update the model
    configuration.model[name] = self.val();
    // mark it as dirty
    configuration.dirty = true;
    // show me
    console.log(self.attr("name") + ": " + configuration.model[name]);
    // all done
    return false;
}


submitAction = function() {
    // save me
    var self = $(this);
    // if the control is disabled
    if (self.hasClass("disabled")) {
        // do nothing
        return false;
    }

    // disable everybody
    $("[action]").addClass("disabled");
    // mark me as the active one
    self.addClass("active");

    // if the model has been modified
    if (configuration.dirty) {
        // send the values to the server
        $.ajax({
            type: "POST",
            url: "/receive",
            data: JSON.stringify(configuration.model),
            async: false,
        });
        // and let me know
        console.log("dirty dirty model");
    }

    // get the behavior
    var behavior = self.attr("action");
    // post
    $.ajax({
        url: "/" + behavior
    }).done(function(data) {
        // enable everybody
        $("[action]").removeClass("disabled");
        // i am not the active one any more
        self.removeClass("active");
        // but i am done
        self.addClass("done");
    });

    // prevent event bubbling
    return false;
}

exitApplication = function() {
    // post the exit request
    $.ajax({
        url: "/shutdown"
    });

    // prevent event bubbling
    return false;
}

// end of file
