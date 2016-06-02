// -*- javascript -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// authors:
//   Michael Aïvázis <michael.aivazis@para-sim.com>
//   Raúl Radovitzky <raul.radovitzky@para-sim.com>
//
// (c) 2013-2016 all rights reserved
//

// {project.name} configuration object
// constructor
function {project.name}_Configuration(name) {{
    // locate the configuration placeholder
    this.element = $(name)

    // make something up
    value = this.buildControls();
    // install
    this.element.html(value);

    // all done
    return
}}

// state
{project.name}_Configuration.prototype.dirty = false;

// build the configuration controls
{project.name}_Configuration.prototype.buildControls = function() {{
    // the control box is an itemized list
    box = [
        //
        '<p>',
        '<table class="{project.name}-controls">',
        //
        '  <tr>',
        '    <th>General settings</th>',
        '  </tr>',
        '  <tr>',
        '    <td class="prompt">site name:</td>',
        '    <td class="field">',
        '      <h2 name="site"/></h2>',
        '    </td>',
        '  </tr>',
        //
        '  <tr>',
        '    <th>Model constraints</th>',
        '  <tr>',
        '  <tr>',
        '    <td class="prompt">horizons:</td>',
        '    <td class="field">',
        '      <input class="list" type="text" name="horizons"/>',
        '    </td>',
        '  </tr>',
        //
        '  <tr>',
        '    <th>Meshing control</th>',
        '  <tr>',
        '    <td class="prompt">resolution:</td>',
        '    <td class="field">',
        '      <input class="float" type="text" name="resolution"/>',
        '    </td>',
        '  </tr>',
        '  <tr>',
        '    <td class="prompt">verbose:</td>',
        '    <td class="field">',
        '      <input class="float" type="text" name="verbose"/>',
        '    </td>',
        '  </tr>',
        '  <tr>',
        '    <td class="prompt">padding:</td>',
        '    <td class="field">',
        '      <input class="list" type="text" name="padding"/>',
        '    </td>',
        '  </tr>',
        // all done with the configuration controls
        '</table>',
        '</p>',

        // actions
        '<p>',
        '<table class="{project.name}-actions">',
        //
        '  <tr>',
        '    <th>Actions</th>',
        '  </tr>',
        '  <tr>',
        '    <td class="prompt">grid:</td>',
        '    <td class="action">',
        //'      <span action="actions/grid/synth">synth</span>',
        '    </td>',
        '    <td class="action">',
        '      <span action="actions/grid/pickle">pickle</span>',
        '    </td>',
        '    <td class="action">',
        '      <span action="actions/grid/stats">stats</span>',
        '    </td>',
        '    <td></td>',
        '    <td class="action">',
        '      <span action="actions/grid/vtu">vtu</span>',
        '    </td>',
        '    <td class="action">',
        '      <span action="actions/grid/help">help</span>',
        '    </td>',
        '  </tr>',
        '  <tr>',
        '    <td class="prompt">mesh:</td>',
        '    <td class="action">',
        '      <span action="actions/mesh/script">script</span>',
        '    </td>',
        '    <td class="action">',
        '      <span action="actions/mesh/box">box</span>',
        '    </td>',
        '    <td class="action">',
        '      <span action="actions/mesh/paint">paint</span>',
        '    </td>',
        '    <td class="action">',
        '      <span action="actions/mesh/summit">summit</span>',
        '    </td>',
        '    <td class="action">',
        '      <span action="actions/mesh/vtu">vtu</span>',
        '    </td>',
        '    <td class="action">',
        '      <span action="actions/mesh/help">help</span>',
        '    </td>',
        '  </tr>',

        '  <tr>',
        '    <td class="prompt">summit:</td>',
        '    <td class="action">',
        '      <span action="actions/summit/overburden">overburden</span>',
        '    </td>',
        '    <td class="action">',
        '      <span action="actions/summit/coupled">coupled</span>',
        '    </td>',
        '    <td class="action">',
        '      <span action="actions/summit/coupled">overburden+coupled</span>',
        '    </td>',
        '  <tr>',

        // all done with the actions
        '</table>',
        '</p>',

        // all done
    ];

    // assemble it
    body = box.join("");
    // all done
    return body;
}}

// behavior
{project.name}_Configuration.prototype.close = function() {{
    // close the current tab
    window.close();
    // prevent event bubbling
    return false;
}}

{project.name}_Configuration.prototype.receive = function(data) {{
    // show me
    console.log("retrieved initial configuration");
    // save the data model
    this.model = $.parseJSON(data);
    // mark it as clean
    this.dirty = false;

    // update
    $('[name="site"]').html(this.model.site);
    $('[name="horizons"]').val(this.model.horizons);
    $('[name="padding"]').val(this.model.padding);
    $('[name="resolution"]').val(this.model.resolution);
    $('[name="verbose"]').val(this.model.verbose);

    // all done
    return;
}}


updateModel = function() {{
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
}}


submitAction = function() {{
    // save me
    var self = $(this);
    // if the control is disabled
    if (self.hasClass("disabled")) {{
        // do nothing
        return false;
    }}

    // disable everybody
    $("[action]").addClass("disabled");
    // mark me as the active one
    self.addClass("active");

    // if the model has been modified
    if (configuration.dirty) {{
        // send the values to the server
        $.ajax({{
            type: "POST",
            url: "/receive",
            data: JSON.stringify(configuration.model),
            async: false,
        }});
        // and let me know
        console.log("dirty dirty model");
    }}

    // get the behavior
    var behavior = self.attr("action");
    // post
    $.ajax({{
        url: "/" + behavior
    }}).done(function(data) {{
        // enable everybody
        $("[action]").removeClass("disabled");
        // i am not the active one any more
        self.removeClass("active");
        // but i am done
        self.addClass("done");
    }});

    // prevent event bubbling
    return false;
}}

exitApplication = function() {{
    // post the exit request
    $.ajax({{
        url: "/shutdown"
    }});

    // prevent event bubbling
    return false;
}}

// end of file
