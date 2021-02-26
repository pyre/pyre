// -*- web -*-
//
// {project.authors}
// (c) {project.span} all rights reserved


// get colors
import {{ theme }} from '~/palette'


// styling for the page container
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
}}


// end of file
