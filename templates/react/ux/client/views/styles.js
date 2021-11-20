// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// get colors
import {{ wheel, theme }} from '~/palette'


// publish
export default {{
    // the top level flex container
    page : {{
        // placement
        width: "100%",
        height: "100%",

        // overall styling
        backgroundColor: theme.page.background,

        // for my children
        display: "flex",
        flexDirection: "column",
    }},

    // the container
    panel: {{
        // my box
        flex: "1",
        position: "relative",
        margin: "0.0em",
        padding: "0.0em",

        // styling
        backgroundColor: theme.page.background,

        // my children
        overflow: "hidden",
        display: "flex",
        flexDirection: "row",
    }},


    // the area with the temporary message for the pages that are under construction
    placeholder: {{
        position: "fixed",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
    }},
}}


// end of file
