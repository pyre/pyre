// -*- web -*-
//
// {project.authors}
// (c) 1998-2020 all rights reserved


// get colors
import {{ wheel, theme }} from '~/palette'
// get the base styles
import base from '~/views/styles'


// publish
export default {{
    // the overall page
    page: {{
        // inherit
        ...base.page,
    }},

    // the container
    panel: {{
        // inherit
        ...base.panel,
        // style
        // no smaller than
        minWidth: "600px",
        minHeight: "400px",
    }},

    flex: {{
        // the overall flex container
        box: {{
            flex: "1 1 auto",
            backgroundColor: "hsl(0deg, 0%, 10%)",
        }},

        // individual panels
        panel: {{
            backgroundColor: "hsl(0deg, 0%, 5%, 1)",
        }},

        // the inter-panel separator
        separator: {{
            // the line
            rule: {{
                backgroundColor: "hsl(0deg, 0%, 15%, 0.5)",
            }},
            // the handle
            handle: {{
            }},
        }},
    }},

    activitybar: {{
        // NYI
        // NOT STYLABLE FROM HERE AT THIS POINT
        // THE ActivityBar DOES NOT PARTICIPATE IN PAINT MIXING
    }},

    sidebar: {{
        // size me
        width: "100%",
        height: "100%",
        // paint
        backgroundColor: "hsl(0deg, 0%, 15%, 1)",
        // shift me a bit
        paddingLeft: "0.25rem",
    }},

    canvas: {{
        // paint
        backgroundColor: "hsl(0deg, 0%, 5%, 1)",
        // occupy all available space
        width: "100%",
        height: "100%",
        // let me strech, initially
        // flex: "4 1 auto",

        // shift me a bit
        paddingLeft: "0.25rem",
    }},
}}


// end of file
